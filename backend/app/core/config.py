from typing import List, Literal
from pydantic import EmailStr, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Acounting API"
    API_PREFIX: str = "/api/v1"
    VERSION: str = "0.1.0"
    DEBUG: bool = True
    ENVIRONMENT: Literal["dev", "prod", "test"] = "dev"

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    ALGORITHM: str = "HS256"

    REFRESH_TOKEN_EXPIRE_DAYS: int = 14

    DATABASE_URL: PostgresDsn
    SYNC_DATABASE_URL: PostgresDsn

    CORS_ORIGINS: List[str] = ["http://localhost:5173"]
    FRONTEND_URL: str = "http://localhost:5173"

    EMAIL_FROM: EmailStr
    EMAIL_FROM_NAME: str = "Acounting"
    EMAIL_SERVER: str
    EMAIL_PORT: int
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_USE_TLS: bool = True
    EMAIL_USE_SSL: bool = False

    FILE_STORAGE_PATH: str = "./storage"

    ENABLE_EINVOICE: bool = True
    ENABLE_ELSTER: bool = False
    ENABLE_BANKING: bool = False

    # APIs
    VIES_WSDL_URL: str = "https://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl"

    # Default admin credentials
    DEFAULT_ADMIN_EMAIL: EmailStr = "admin@example.com"
    DEFAULT_ADMIN_PASSWORD: str = "gotta_change_this"
    DEFAULT_ADMIN_FIRST_NAME: str = "Admin"
    DEFAULT_ADMIN_LAST_NAME: str = "User"


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings() # type: ignore
