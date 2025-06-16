from typing import Optional, Literal
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    preferred_language: Literal["en", "de"] = "en"
    preferred_currency: Literal["EUR", "USD", "CHF"] = "EUR"
    is_active: bool = True
    is_verified: bool = False
    role: Literal["owner", "accountant", "viewer"] = "owner"

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    preferred_language: Optional[Literal["en", "de"]] = None
    preferred_currency: Optional[Literal["EUR", "USD", "CHF"]] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    role: Optional[Literal["owner", "accountant", "viewer"]] = None
    password: Optional[str] = Field(None, min_length=8)

    model_config = ConfigDict(from_attributes=True)


class UserRead(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
