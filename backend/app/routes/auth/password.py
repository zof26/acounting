from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Annotated
from datetime import timedelta

from sqlmodel import select
from app.db.session import get_session
from app.models.user import User
from app.models.password import (
    PasswordChange,
    PasswordResetRequest,
    PasswordResetConfirm,
)
from app.core.security import (
    get_current_user,
    verify_password,
    create_access_token,
    decode_access_token,
)
from app.crud.user import update_user_password
from app.core.config import settings
from app.services.email import send_password_reset_email 

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/change-password", status_code=204)
async def change_password(
    data: PasswordChange,
    user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_session),
):
    if not verify_password(data.old_password, user.hashed_password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid current password")

    await update_user_password(db, user, data.new_password)


@router.post("/forgot-password", status_code=202)
async def forgot_password(
    data: PasswordResetRequest,
    db: AsyncSession = Depends(get_session),
):
    result = await db.exec(select(User).where(User.email == data.email))
    user = result.one_or_none()

    if not user:
        return  # Don't leak account existence

    token = create_access_token(
        {"sub": user.email, "purpose": "reset_password"},
        expires_delta=timedelta(minutes=15),
    )

    await send_password_reset_email(user.email, token)


@router.post("/reset-password", status_code=204)
async def reset_password(
    data: PasswordResetConfirm,
    db: AsyncSession = Depends(get_session),
):
    payload = decode_access_token(data.token)

    if payload.get("purpose") != "reset_password":
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid token")

    email = payload.get("sub")
    if not email:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Malformed token")

    result = await db.exec(select(User).where(User.email == email))
    user = result.one_or_none()

    if not user or not user.is_active:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

    await update_user_password(db, user, data.new_password)
