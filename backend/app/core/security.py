from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jwt.exceptions import InvalidTokenError
from jwt import ExpiredSignatureError
from typing import Optional

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.enums import RoleEnum 
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

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except InvalidTokenError:
        raise credentials_exception


async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[User]:
    result = await db.exec(select(User).where(User.email == email))
    user = result.one_or_none()
    
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user if user.is_active else None

async def get_current_user(
        token: Annotated[str,  Depends(oauth2_scheme)], 
        db: Annotated[AsyncSession, Depends(get_session)]
    ) -> User:
    payload = decode_access_token(token)
    
    if payload.get("scope") != "auth":
        raise credentials_exception
    
    email = payload.get("sub")
    if not email or not isinstance(email, str):
        raise credentials_exception
    
    result = await db.exec(select(User).where(User.email == email))
    user = result.one_or_none()
    if not user or not user.is_active:
        raise credentials_exception
    return user

def require_roles(allowed_roles: list[RoleEnum]):
    async def wrapper(user: User = Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return user
    return wrapper
