from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, ConfigDict


class ItemType(str, Enum):
    service = "service"
    product = "product"
    bundle = "bundle"


# === ORM Model ===
class Item(SQLModel, table=True):
    __tablename__ = "item"  # type: ignore

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

    name: str = Field(max_length=512)
    description: Optional[str] = Field(default=None)
    type: ItemType = Field(default=ItemType.service)

    unit: Optional[str] = Field(default="hour", max_length=50)  # e.g., "hour", "piece", "day"
    unit_price: Decimal = Field(default=Decimal("0.0"), ge=0, decimal_places=2)
    cost_price: Optional[Decimal] = Field(default=Decimal("0.0"), ge=0, decimal_places=2)
    vat_rate: Decimal = Field(default=Decimal("19.0"), ge=0, le=100)

    external_id: Optional[str] = Field(default=None, max_length=100)  # for SKU, shop sync, etc.

    is_active: bool = Field(default=True)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    def touch(self):
        """Update the `updated_at` timestamp manually."""
        self.updated_at = datetime.now(timezone.utc)


# === Pydantic Schemas ===

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: ItemType = ItemType.service

    unit: Optional[str] = "hour"
    unit_price: Decimal
    cost_price: Optional[Decimal] = Decimal("0.0")
    vat_rate: Decimal = Decimal("19.0")

    external_id: Optional[str] = None
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[ItemType] = None

    unit: Optional[str] = None
    unit_price: Optional[Decimal] = None
    cost_price: Optional[Decimal] = None
    vat_rate: Optional[Decimal] = None

    external_id: Optional[str] = None
    is_active: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class ItemRead(ItemBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
