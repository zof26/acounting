from datetime import datetime, timedelta, timezone
from uuid import uuid4
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.core.config import settings
from app.models.refresh_token import RefreshToken

REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS

async def create_refresh_token(db: AsyncSession, user_id) -> RefreshToken:
    token_value = str(uuid4())
    expires_at = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    token = RefreshToken(
        user_id=user_id,
        token=token_value,
        expires_at=expires_at,
    )

    db.add(token)
    await db.commit()
    await db.refresh(token)
    return token

async def get_refresh_token(db: AsyncSession, token_str: str) -> RefreshToken | None:
    result = await db.exec(
        select(RefreshToken).where(RefreshToken.token == token_str)
    )
    return result.one_or_none()

async def revoke_token(db: AsyncSession, token: RefreshToken) -> None:
    token.revoked = True
    await db.commit()
