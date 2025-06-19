from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from app.models.enums import ClientTypeEnum
from app.schemas.contact_person import ContactPersonCreate
from app.schemas.document_attachment import DocumentAttachmentCreate
from app.schemas.contact_person import ContactPersonRead
from app.schemas.document_attachment import DocumentAttachmentRead

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
    contacts: Optional[List[ContactPersonCreate]] = Field(default_factory=list)
    attachments: Optional[List[DocumentAttachmentCreate]] = Field(default_factory=list)

class ClientUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=512)
    type: Optional[ClientTypeEnum] = None
    ust_id: Optional[str] = Field(None, max_length=20)
    ust_id_validated: Optional[bool] = None
    ust_id_checked_at: Optional[datetime] = None
    notes: Optional[str] = None
    dunning_level: Optional[int] = Field(None, ge=0, le=3)
    is_active: Optional[bool] = None
    contacts: Optional[List[ContactPersonCreate]] = Field(default_factory=list)
    attachments: Optional[List[DocumentAttachmentCreate]] = Field(default_factory=list)


    model_config = ConfigDict(from_attributes=True)

class ClientRead(ClientBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    contacts: List[ContactPersonRead] = Field(default_factory=list)
    attachments: List[DocumentAttachmentRead] = Field(default_factory=list)


    model_config = ConfigDict(from_attributes=True)
