from sqlmodel import SQLModel, Field
from uuid import uuid4, UUID
from datetime import datetime, timezone
from sqlalchemy import TIMESTAMP, Column

class RefreshToken(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: UUID = Field(index=True, nullable=False)
    token: str = Field(unique=True, index=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False)
    )
    expires_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False)
    )    
    revoked: bool = Field(default=False)

    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) >= self.expires_at
