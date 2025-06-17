from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Annotated

from app.core.security import get_current_user, verify_password, hash_password
from app.db.session import get_session
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate
from app.schemas.password import PasswordChange
from app.crud.user import update_user_password, update_user_self

router = APIRouter(prefix="/users/me", tags=["users"])

@router.get("", response_model=UserRead, summary="Get current user profile")
async def get_profile(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user

@router.patch("", response_model=UserRead, summary="Update current user profile")
async def update_profile(
    data: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    # Prevent editing restricted fields
    if "role" in data.model_fields_set or "is_active" in data.model_fields_set:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not allowed to update 'role' or 'is_active'.")

    updated_user = await update_user_self(db, current_user, data)
    return updated_user

@router.post("/password", status_code=204, summary="Change your password")
async def change_password(
    data: PasswordChange,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    if not verify_password(data.old_password, current_user.hashed_password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid current password")

    await update_user_password(db, current_user, data.new_password)
