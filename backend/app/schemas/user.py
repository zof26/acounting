from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from app.models.enums import LanguageEnum, CurrencyEnum, RoleEnum


class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    preferred_language: LanguageEnum = LanguageEnum.en
    preferred_currency: CurrencyEnum = CurrencyEnum.EUR
    role: RoleEnum = RoleEnum.Accountant
    is_active: bool = True
    is_verified: bool = False
    
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserPasswordUpdate(BaseModel):
    password: str = Field(min_length=8)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    preferred_language: Optional[LanguageEnum] = None
    preferred_currency: Optional[CurrencyEnum] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    role: Optional[RoleEnum] = None

    model_config = ConfigDict(from_attributes=True)


class UserRead(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    preferences: Optional[dict] = Field(default_factory=dict)
    onboarding_completed: bool = False

    model_config = ConfigDict(from_attributes=True)
