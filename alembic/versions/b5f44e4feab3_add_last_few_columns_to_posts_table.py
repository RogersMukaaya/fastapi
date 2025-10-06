"""add last few columns to posts table

Revision ID: b5f44e4feab3
Revises: c1b946398b83
Create Date: 2025-10-06 11:39:48.676607

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5f44e4feab3'
down_revision: Union[str, Sequence[str], None] = 'c1b946398b83'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False, server_default='TRUE'))

    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))

    pass


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')

    pass
