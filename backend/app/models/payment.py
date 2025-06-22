from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4
from datetime import datetime, timezone
from decimal import Decimal

from sqlmodel import SQLModel, Field, Column, Relationship
from sqlalchemy import DateTime
from pydantic import BaseModel, ConfigDict
from app.models.enums import PaymentMethodEnum
from sqlalchemy import Enum as SAEnum

if TYPE_CHECKING:
    from app.models.invoice import Invoice


# ==== ORM Model ====

class Payment(SQLModel, table=True):
    __tablename__ = "payment"  # type: ignore[assignment]

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

    invoice_id: UUID = Field(foreign_key="invoice.id", nullable=False)
    invoice: "Invoice" = Relationship(back_populates="payments")

    method: Optional[PaymentMethodEnum] = Field(default=None)  
    transaction_id: Optional[str] = Field(default=None, max_length=128) 

    amount: Decimal = Field(decimal_places=2, ge=0)
    received_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )

    notes: Optional[str] = Field(default=None)

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

class PaymentBase(BaseModel):
    invoice_id: UUID
    amount: Decimal
    method: Optional[PaymentMethodEnum] = None
    transaction_id: Optional[str] = None
    received_at: Optional[datetime] = None
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    amount: Optional[Decimal] = None
    method: Optional[PaymentMethodEnum] = None
    transaction_id: Optional[str] = None
    received_at: Optional[datetime] = None
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class PaymentRead(PaymentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
