from typing import Optional, List, TYPE_CHECKING
from uuid import UUID, uuid4
from datetime import datetime, timezone

from sqlmodel import SQLModel, Field, Column, Relationship
from sqlalchemy import DateTime, Enum as SAEnum, String
from pydantic import BaseModel, ConfigDict

from app.models.enums import InvoiceStatusEnum, CurrencyEnum, LanguageEnum
from app.models.invoice_item import InvoiceItemCreate, InvoiceItemRead
from app.models.client import ClientRead

if TYPE_CHECKING:
    from app.models.invoice_item import InvoiceItem
    from app.models.client import Client
    from app.models.payment import Payment


# ==== ORM Model ====

class Invoice(SQLModel, table=True):
    __tablename__ = "invoice"  # type: ignore[assignment]

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    number: str = Field(nullable=False, unique=True, index=True, max_length=64)

    client_id: UUID = Field(foreign_key="client.id", nullable=False)
    client: "Client" = Relationship(back_populates="invoices")

    issue_date: datetime
    due_date: datetime
    paid_at: Optional[datetime] = None
    dunning_level: int = Field(default=0, ge=0, le=3)
    dunning_fee: float = Field(default=0.0, ge=0.0)
    reminder_count: int = Field(default=0, ge=0)
    last_reminder_sent_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )

    payments: List["Payment"] = Relationship(
        back_populates="invoice",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    status: InvoiceStatusEnum = Field(
        sa_column=Column(SAEnum(InvoiceStatusEnum, name="invoicestatusenum", native_enum=True, create_type=True))
    )
    currency: CurrencyEnum = Field(sa_column=Column(String(3)))
    language: LanguageEnum = Field(sa_column=Column(String(2)))

    subtotal: float
    vat: float
    total: float

    reverse_charge: bool = False
    oss: bool = False

    notes: Optional[str] = None
    terms: Optional[str] = None
    attachment_url: Optional[str] = Field(default=None, max_length=2048)

    items: List["InvoiceItem"] = Relationship(
        back_populates="invoice",
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
        self.updated_at = datetime.now(timezone.utc)


# ==== Pydantic Schemas ====

class InvoiceBase(BaseModel):
    number: str
    client_id: UUID
    issue_date: datetime
    due_date: datetime
    paid_at: Optional[datetime] = None
    status: InvoiceStatusEnum
    currency: CurrencyEnum
    language: LanguageEnum
    dunning_level: int = 0
    dunning_fee: float = 0.0
    reminder_count: int = 0
    last_reminder_sent_at: Optional[datetime] = None
    subtotal: float
    vat: float
    total: float
    reverse_charge: bool = False
    oss: bool = False
    notes: Optional[str] = None
    terms: Optional[str] = None
    attachment_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class InvoiceCreate(InvoiceBase):
    items: List[InvoiceItemCreate] = Field(default_factory=list)

class InvoiceUpdate(BaseModel):
    number: Optional[str] = None
    client_id: Optional[UUID] = None
    issue_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    paid_at: Optional[datetime] = None
    status: Optional[InvoiceStatusEnum] = None
    currency: Optional[CurrencyEnum] = None
    language: Optional[LanguageEnum] = None
    dunning_level: Optional[int] = None
    dunning_fee: Optional[float] = None
    reminder_count: Optional[int] = None
    last_reminder_sent_at: Optional[datetime] = None
    subtotal: Optional[float] = None
    vat: Optional[float] = None
    total: Optional[float] = None
    reverse_charge: Optional[bool] = None
    oss: Optional[bool] = None
    notes: Optional[str] = None
    terms: Optional[str] = None
    attachment_url: Optional[str] = None
    items: Optional[List[InvoiceItemCreate]] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class InvoiceRead(InvoiceBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    items: List[InvoiceItemRead] = Field(default_factory=list)
    client: ClientRead
    payments: List[Payment] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)
