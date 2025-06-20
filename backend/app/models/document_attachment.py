from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from uuid import UUID, uuid4
from datetime import datetime, timezone
import sqlalchemy as sa
from sqlmodel import SQLModel
from sqlalchemy import Column, DateTime
from pydantic import BaseModel, ConfigDict

# ==== ORM model ====
if TYPE_CHECKING:
    from app.models.client import Client


class DocumentAttachment(SQLModel, table=True):
    __tablename__ = "document_attachment" # type: ignore[assignment]
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

    client_id: UUID = Field(foreign_key="client.id", nullable=False, index=True)

    file_name: str = Field(nullable=False, max_length=255)
    file_type: Optional[str] = Field(default=None, max_length=100)
    file_url: str = Field(nullable=False, max_length=512)

    uploaded_by: Optional[str] = Field(default=None, max_length=100)
    uploaded_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=sa.Column(sa.TIMESTAMP(timezone=True), nullable=False)
    )

    notes: Optional[str] = Field(default=None)
    client: Optional["Client"] = Relationship(back_populates="attachments")

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

# ==== Pydantic schemas ====

class DocumentAttachmentBase(BaseModel):
    file_name: str = Field(..., max_length=255)
    file_type: Optional[str] = Field(None, max_length=100)
    file_url: str = Field(..., max_length=512)
    uploaded_by: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class DocumentAttachmentCreate(DocumentAttachmentBase):
    client_id: Optional[UUID] = None

class DocumentAttachmentRead(DocumentAttachmentBase):
    id: UUID
    client_id: UUID
    uploaded_at: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)