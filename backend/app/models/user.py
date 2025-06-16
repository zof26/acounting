from typing import Optional, List, Literal
from sqlmodel import SQLModel, Field, Column, JSON
from uuid import UUID, uuid4
from datetime import datetime, timezone
from app.models.base import BaseModel


class User(BaseModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

    email: str = Field(index=True, nullable=False, unique=True, max_length=320)
    hashed_password: str = Field(nullable=False)

    first_name: Optional[str] = Field(default=None, max_length=50)
    last_name: Optional[str] = Field(default=None, max_length=50)

    language: str = Field(default="en", max_length=5)  
    currency: str = Field(default="EUR", max_length=5)

    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    roles: List[str] = Field(default_factory=list, sa_column=Column(JSON))

    last_login: Optional[datetime] = Field(default=None)
    preferences: Optional[dict] = Field(default_factory=dict, sa_column=Column(JSON))

    onboarding_completed: bool = Field(default=False)
