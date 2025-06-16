from pydantic import BaseSettings, EmailStr, AnyHttpUrl, PostgresDsn, field_validator
from typing import List, Literal
import os

class Settings(BaseSettings):
    # App Info
    PROJECT_NAME: str = "Acounting API"
    API_PREFIX: str = "/api/v1"
    VERSION: str = "0.1.0"
    DEBUG: bool = False
    ENVIRONMENT: Literal["dev", "prod", "test"] = "dev"

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    ALGORITHM: str = "HS256"

    # Database
    DATABASE_URL: PostgresDsn

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def split_origins(cls, v):
        if isinstance(v, str):
            return [s.strip() for s in v.split(",")]
        return v
    
    # Email
    EMAIL_FROM: EmailStr
    EMAIL_FROM_NAME: str = "Acounting"
    EMAIL_SERVER: str
    EMAIL_PORT: int
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_USE_TLS: bool = True
    EMAIL_USE_SSL: bool = False

    # File storage
    FILE_STORAGE_PATH: str = "./storage"

    # Feature toggles
    ENABLE_EINVOICE: bool = True
    ENABLE_ELSTER: bool = False
    ENABLE_BANKING: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
