from typing import Optional
from sqlmodel import Field, Column, JSON, SQLModel
from uuid import UUID, uuid4
from datetime import datetime, timezone
from app.models.enums import RoleEnum
import sqlalchemy as sa
from sqlalchemy import Column, DateTime, String
from pydantic import BaseModel, EmailStr, ConfigDict


# ==== ORM model =====
class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

    email: str = Field(index=True, nullable=False, unique=True, max_length=320)
    hashed_password: str = Field(nullable=False)

    first_name: str = Field(default=None, max_length=50)
    last_name: str = Field(default=None, max_length=50)

    role: RoleEnum = Field(sa_column=Column(String(20)), default=RoleEnum.Accountant)  
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

# ==== Pydantic schemas =====

class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    role: RoleEnum = RoleEnum.Accountant
    
    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    is_active: bool = True

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)

    model_config = ConfigDict(from_attributes=True)

class UserAdminUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    role: Optional[RoleEnum] = None
    is_active: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)

class UserRead(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    preferences: Optional[dict] = Field(default_factory=dict)
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
