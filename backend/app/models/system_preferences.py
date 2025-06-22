from typing import Optional
from uuid import UUID
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Column
from pydantic import BaseModel, HttpUrl, ConfigDict, model_validator
from sqlalchemy import DateTime
from app.models.enums import CurrencyEnum, LanguageEnum, TaxSchemeEnum

# ==== ORM model ====
STATIC_ID = UUID("00000000-0000-0000-0000-000000000001")

class SystemPreferences(SQLModel, table=True):
    __tablename__ = "system_preferences"  # type: ignore[assignment]

    id: UUID = Field(default=STATIC_ID, primary_key=True, index=True)

    company_name: str = Field(max_length=512)
    company_logo_url: Optional[str] = Field(default=None, nullable=True, max_length=2048)

    default_currency: CurrencyEnum
    default_language: LanguageEnum
    tax_scheme: TaxSchemeEnum

    invoice_prefix: Optional[str] = Field(default="INV", max_length=16)
    enable_reverse_charge: bool = False
    enable_oss: bool = False

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


# ==== Pydantic schemas ====

class SystemPreferencesBase(BaseModel):
    company_name: str = Field(max_length=512)
    company_logo_url: Optional[HttpUrl] = None

    default_currency: CurrencyEnum
    default_language: LanguageEnum
    tax_scheme: TaxSchemeEnum

    invoice_prefix: Optional[str] = Field(default="INV", max_length=16)
    enable_reverse_charge: bool = False
    enable_oss: bool = False

    model_config = ConfigDict(from_attributes=True)


class SystemPreferencesCreate(SystemPreferencesBase):

    @model_validator(mode="after")
    def validate_tax_logic(self) -> "SystemPreferencesCreate":
        if self.tax_scheme == TaxSchemeEnum.kleinunternehmer and self.enable_oss:
            raise ValueError("OSS cannot be enabled under the Kleinunternehmerregelung.")
        return self

class SystemPreferencesUpdate(BaseModel):
    company_name: Optional[str] = Field(None, max_length=512)
    company_logo_url: Optional[HttpUrl] = Field(default=None, nullable=True)

    default_currency: Optional[CurrencyEnum] = Field(default=None)
    default_language: Optional[LanguageEnum] = Field(default=None)
    tax_scheme: Optional[TaxSchemeEnum] = Field(default=None)

    invoice_prefix: Optional[str] = Field(None, max_length=16)
    enable_reverse_charge: Optional[bool] = Field(default=None)
    enable_oss: Optional[bool] = Field(default=None)

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def validate_tax_logic(self) -> "SystemPreferencesUpdate":
        if self.tax_scheme == TaxSchemeEnum.kleinunternehmer and self.enable_oss:
            raise ValueError("OSS cannot be enabled under the Kleinunternehmerregelung.")
        return self


class SystemPreferencesRead(SystemPreferencesBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
