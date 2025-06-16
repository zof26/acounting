from datetime import datetime, timezone
from sqlmodel import SQLModel, Field


class BaseModel(SQLModel):
    """Base class for all models with standard audit fields."""

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def touch(self):
        """Manually update `updated_at` to current UTC time."""
        self.updated_at = datetime.now(timezone.utc)
