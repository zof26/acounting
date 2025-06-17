from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jwt.exceptions import InvalidTokenError

from typing import Optional, List

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.core.config import settings
from app.models.user import User
from app.db.session import get_session

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
SECRET_KEY = settings.SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/auth/token")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except InvalidTokenError:
        raise credentials_exception


async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[User]:
    result = await db.exec(select(User).where(User.email == email))
    user = result.one_or_none()
    
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user if user.is_active else None

async def get_current_user(token: Annotated[str,  Depends(oauth2_scheme)], db: Annotated[AsyncSession, Depends(get_session)]) -> User:
    payload = decode_access_token(token)
    
    email = payload.get("sub")
    if not email or not isinstance(email, str):
        raise credentials_exception
    
    result = await db.exec(select(User).where(User.email == email))
    user = result.one_or_none()
    if not user or not user.is_active:
        raise credentials_exception
    return user

def require_roles(roles: List[str]):
    async def wrapper(u: User = Depends(get_current_user)):
        if u.role.value not in roles:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Insufficient permissions")
        return u
    return wrapper
