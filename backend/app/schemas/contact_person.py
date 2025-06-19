from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import datetime

class ContactPersonBase(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email: Optional[EmailStr] = Field(None, max_length=320)
    phone: Optional[str] = Field(None, max_length=50)
    mobile: Optional[str] = Field(None, max_length=50)
    position: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None
    is_main_contact: bool = True

    model_config = ConfigDict(from_attributes=True)

class ContactPersonCreate(ContactPersonBase):
    pass

class ContactPersonUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = Field(None, max_length=320)
    phone: Optional[str] = Field(None, max_length=50)
    mobile: Optional[str] = Field(None, max_length=50)
    position: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None
    is_main_contact: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)

class ContactPersonRead(ContactPersonBase):
    id: UUID
    client_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
