from sqlmodel import Session, SQLModel, create_engine
from app.core.config import settings
from typing import Generator

# Create the engine
engine = create_engine(
    str(settings.DATABASE_URL),
    echo=settings.DEBUG,
    pool_pre_ping=True,
)

# Session dependency
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

# For testing overrides / CLI tools
def get_engine():
    return engine

# For Alembic
def get_metadata():
    return SQLModel.metadata
