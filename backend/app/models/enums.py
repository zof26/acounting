from enum import Enum

class LanguageEnum(str, Enum):
    en = "en"
    de = "de"

class CurrencyEnum(str, Enum):
    EUR = "EUR"
    USD = "USD"
    CHF = "CHF"

class RoleEnum(str, Enum):
    Admin = "Admin"
    Accountant = "Accountant"

class ClientTypeEnum(str, Enum):
    client = "Client"
    prospect = "Prospect"
    lead = "Lead"

class TaxSchemeEnum(str, Enum):
    kleinunternehmer = "Kleinunternehmer"
    vat_liable = "VAT liable"


class InvoiceStatusEnum(str, Enum):
    draft = "draft"
    sent = "sent"
    paid = "paid"
    overdue = "overdue"
    cancelled = "cancelled"

class PaymentMethodEnum(str, Enum):
    sepa = "SEPA"
    stripe = "Stripe"
    paypal = "PayPal"
    cash = "Cash"
    bank_transfer = "International Bank Transfer"