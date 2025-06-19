from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from uuid import UUID, uuid4
from sqlmodel import SQLModel
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime


if TYPE_CHECKING:
    from app.models.client import Client

class ContactPerson(SQLModel, table=True):
    __tablename__ = "contact_person" # type: ignore[assignment]
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    client_id: UUID = Field(foreign_key="client.id", nullable=False, index=True)

    first_name: str = Field(nullable=False, max_length=50)
    last_name: str = Field(nullable=False, max_length=50)
    email: Optional[str] = Field(default=None, max_length=320, index=True)
    phone: Optional[str] = Field(default=None, max_length=50)
    mobile: Optional[str] = Field(default=None, max_length=50)
    position: Optional[str] = Field(default=None, max_length=100)
    notes: Optional[str] = Field(default=None)

    is_main_contact: bool = Field(default=True)

    client: Optional["Client"] = Relationship(back_populates="contacts")

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