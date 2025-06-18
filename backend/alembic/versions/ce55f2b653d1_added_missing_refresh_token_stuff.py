"""added missing refresh token stuff

Revision ID: ce55f2b653d1
Revises: 1b6bfa5d666d
Create Date: 2025-06-18 21:55:25.414091

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce55f2b653d1'
down_revision: Union[str, None] = '1b6bfa5d666d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
