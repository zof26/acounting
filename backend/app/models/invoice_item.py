from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4
from datetime import datetime, timezone

from sqlmodel import SQLModel, Field, Column, Relationship
from sqlalchemy import DateTime
from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from app.models.invoice import Invoice
    from app.models.item import Item


# ==== ORM Model ====

class InvoiceItem(SQLModel, table=True):
    __tablename__ = "invoice_item" # type: ignore

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

    invoice_id: UUID = Field(foreign_key="invoice.id", nullable=False)
    invoice: "Invoice" = Relationship(
        back_populates="items",
        sa_relationship_kwargs={"order_by": "InvoiceItem.position"}
    )

    item_id: Optional[UUID] = Field(default=None, foreign_key="item.id")
    item: Optional["Item"] = Relationship()

    description: str = Field(max_length=1024)
    quantity: float = Field(ge=0.0)
    unit_price: float = Field(ge=0.0)
    vat_rate: float = Field(default=0.0, ge=0.0)

    position: Optional[int] = Field(default=None, ge=0)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )

    def touch(self):
        self.updated_at = datetime.now(timezone.utc)

# ==== Pydantic Schemas ====

class InvoiceItemBase(BaseModel):
    item_id: Optional[UUID] = None
    description: str
    quantity: float
    unit_price: float
    vat_rate: float = 0.0
    position: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class InvoiceItemCreate(InvoiceItemBase):
    pass

class InvoiceItemUpdate(BaseModel):
    item_id: Optional[UUID] = None
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    vat_rate: Optional[float] = None
    position: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class InvoiceItemRead(InvoiceItemBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
