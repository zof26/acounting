from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, Column, Relationship
from uuid import UUID, uuid4
from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict
import sqlalchemy as sa
from sqlalchemy import Column, DateTime, String
from sqlmodel import SQLModel
from app.models.enums import ClientTypeEnum
from app.models.contact_person import ContactPersonCreate
from app.models.document_attachment import DocumentAttachmentCreate
from app.models.contact_person import ContactPersonRead
from app.models.document_attachment import DocumentAttachmentRead


# ==== ORM model ====
if TYPE_CHECKING:
    from app.models.contact_person import ContactPerson
    from app.models.document_attachment import DocumentAttachment
    from app.models.invoice import Invoice

class Client(SQLModel, table=True):
    __tablename__ = "client" # type: ignore[assignment]
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

    name: str = Field(nullable=False, max_length=512)
    type: ClientTypeEnum = Field(sa_column=Column(String(20)), default=ClientTypeEnum.client)
    ust_id: Optional[str] = Field(default=None, max_length=20)
    ust_id_validated: Optional[bool] = Field(default=False)
    ust_id_checked_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(sa.TIMESTAMP(timezone=True))
    )

    invoices: List["Invoice"] = Relationship(back_populates="client")

    notes: Optional[str] = Field(default=None)
    dunning_level: Optional[int] = Field(default=0, ge=0, le=3)
    is_active: bool = Field(default=True)

    # Relationships
    contacts: List["ContactPerson"] = Relationship(
        back_populates="client",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    attachments: List["DocumentAttachment"] = Relationship(
        back_populates="client",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

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

class VATValidationResponse(BaseModel):
    valid: bool
    name: Optional[str]
    address: Optional[str]
    checked_at: datetime
    note: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
