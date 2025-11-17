"""Add published and created for Posts table

Revision ID: 8db4848b6fd3
Revises: d4f6f57b7ff4
Create Date: 2025-11-15 18:27:38.157336

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8db4848b6fd3"
down_revision: Union[str, Sequence[str], None] = "d4f6f57b7ff4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "posts",
        sa.Column(
            "published", sa.Boolean(), nullable=False, server_default=sa.text("TRUE")
        ),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
