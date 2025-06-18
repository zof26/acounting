from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class DocumentAttachmentBase(BaseModel):
    file_name: str = Field(..., max_length=255)
    file_type: Optional[str] = Field(None, max_length=100)
    file_url: str = Field(..., max_length=512)
    uploaded_by: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class DocumentAttachmentCreate(DocumentAttachmentBase):
    client_id: UUID

class DocumentAttachmentRead(DocumentAttachmentBase):
    id: UUID
    client_id: UUID
    uploaded_at: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
