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
