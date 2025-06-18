from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from app.models.enums import ClientTypeEnum

class ClientBase(BaseModel):
    name: str = Field(..., max_length=512)
    type: ClientTypeEnum = ClientTypeEnum.client
    ust_id: Optional[str] = Field(None, max_length=20)
    ust_id_validated: bool = False
    ust_id_checked_at: Optional[datetime] = None
    notes: Optional[str] = None
    dunning_level: int = Field(default=0, ge=0, le=3)
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=512)
    type: Optional[ClientTypeEnum] = None
    ust_id: Optional[str] = Field(None, max_length=20)
    ust_id_validated: Optional[bool] = None
    ust_id_checked_at: Optional[datetime] = None
    notes: Optional[str] = None
    dunning_level: Optional[int] = Field(None, ge=0, le=3)
    is_active: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)

class ClientRead(ClientBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
