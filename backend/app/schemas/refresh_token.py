from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class RefreshTokenCreate(BaseModel):
    user_id: UUID
    token: str
    expires_at: datetime

class RefreshTokenRead(BaseModel):
    token: str
    expires_at: datetime

class RefreshRequest(BaseModel):
    refresh_token: str

class TokenRefreshResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int