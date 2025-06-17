from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_session
from app.models.user import User
from app.core.config import settings
from app.core.security import authenticate_user, create_access_token, get_current_user, credentials_exception
from app.crud.refresh_token import create_refresh_token

import logging
logger = logging.getLogger("auth")

router = APIRouter(prefix="/auth", tags=["auth"])

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

@router.post("/token", response_model=TokenResponse, summary="Login and return JWT + refresh token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_session)],
) -> TokenResponse:
    user = await authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise credentials_exception

    from datetime import datetime, timezone
    user.last_login = datetime.now(timezone.utc)
    await db.commit()

    access_token = create_access_token(data={"sub": user.email, "scope": "auth"})
    refresh_token = await create_refresh_token(db, user.id)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token.token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

@router.get("/me", response_model=User, summary="Get current authenticated user")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user

@router.post("/logout", status_code=204, summary="Logout (client-side only)")
async def logout():
    return
