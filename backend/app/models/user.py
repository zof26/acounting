from typing import Optional
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime, timezone
from app.models.base import BaseModel


class User(BaseModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    
    email: str = Field(index=True, nullable=False, unique=True, max_length=320)
    hashed_password: str = Field(nullable=False)

    full_name: Optional[str] = Field(default=None, max_length=100)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)

    last_login: Optional[datetime] = Field(default=None)
    preferences: Optional[dict] = Field(default_factory=dict, sa_column_kwargs={"nullable": True})
