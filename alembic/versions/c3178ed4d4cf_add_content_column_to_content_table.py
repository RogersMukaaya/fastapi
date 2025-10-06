"""add content column to content table

Revision ID: c3178ed4d4cf
Revises: 03165d52009c
Create Date: 2025-10-03 15:42:08.044628

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3178ed4d4cf'
down_revision: Union[str, Sequence[str], None] = '03165d52009c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))

    pass


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("posts", "content")
    pass
