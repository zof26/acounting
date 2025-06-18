from typing import Optional
from sqlmodel import Field, Column, JSON
from uuid import UUID, uuid4
from datetime import datetime, timezone
from sqlmodel import SQLModel
from app.models.enums import LanguageEnum, CurrencyEnum, RoleEnum
import sqlalchemy as sa
from sqlalchemy import Column, DateTime

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

    email: str = Field(index=True, nullable=False, unique=True, max_length=320)
    hashed_password: str = Field(nullable=False)

    first_name: str = Field(default=None, max_length=50)
    last_name: str = Field(default=None, max_length=50)

    preferred_language: LanguageEnum = Field(default=LanguageEnum.en)
    preferred_currency: CurrencyEnum = Field(default=CurrencyEnum.EUR)

    role: RoleEnum = Field(default=RoleEnum.Accountant)  

    is_active: bool = Field(default=True)    

    last_login: Optional[datetime] = Field(default=None, sa_column=Column(sa.TIMESTAMP(timezone=True)))
    preferences: Optional[dict] = Field(default_factory=dict, sa_column=Column(JSON))

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )

    def touch(self):
        """Manually update `updated_at` to current UTC time."""
        self.updated_at = datetime.now(timezone.utc)