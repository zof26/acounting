from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, Column, Relationship
from uuid import UUID, uuid4
from datetime import datetime, timezone

import sqlalchemy as sa
from sqlalchemy import Column, DateTime
from sqlmodel import SQLModel
from app.models.enums import ClientTypeEnum

if TYPE_CHECKING:
    from app.models.contact_person import ContactPerson
    from app.models.document_attachment import DocumentAttachment

class Client(SQLModel, table=True):
    __tablename__ = "client" # type: ignore[assignment]
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

    name: str = Field(nullable=False, max_length=255)
    type: ClientTypeEnum = Field(default=ClientTypeEnum.client)

    ust_id: Optional[str] = Field(default=None, max_length=20)
    ust_id_validated: bool = Field(default=False)
    ust_id_checked_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(sa.TIMESTAMP(timezone=True))
    )

    notes: Optional[str] = Field(default=None)
    dunning_level: int = Field(default=0, ge=0, le=3)
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