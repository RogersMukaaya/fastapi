"""create user table

Revision ID: 363d2e38b1e6
Revises: c3178ed4d4cf
Create Date: 2025-10-03 15:53:52.540990

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '363d2e38b1e6'
down_revision: Union[str, Sequence[str], None] = 'c3178ed4d4cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users", 
        sa.Column("id", sa.Integer(), nullable=False), 
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email")
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("users")
    pass
