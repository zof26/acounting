from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.db.session import get_session
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.schemas.refresh_token import RefreshRequest, TokenRefreshResponse
from app.crud.refresh_token import (
    get_refresh_token,
    revoke_token,
    create_refresh_token,
)
from app.core.security import create_access_token
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/refresh", response_model=TokenRefreshResponse, summary="Refresh access token using a valid refresh token")
async def refresh_token_endpoint(
    payload: RefreshRequest,
    db: AsyncSession = Depends(get_session),
):
    stored_token = await get_refresh_token(db, payload.refresh_token)

    if not stored_token or stored_token.revoked or stored_token.is_expired():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    # Fetch user
    user_result = await db.exec(select(User).where(User.id == stored_token.user_id))
    user = user_result.one_or_none()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User inactive or not found",
        )

    # Rotate refresh token
    await revoke_token(db, stored_token)
    new_refresh = await create_refresh_token(db, user.id)
    new_access_token = create_access_token(data={"sub": user.email})

    return TokenRefreshResponse(
        access_token=new_access_token,
        refresh_token=new_refresh.token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
