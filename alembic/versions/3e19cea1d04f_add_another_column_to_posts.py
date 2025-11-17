"""Add another column to Posts

Revision ID: 3e19cea1d04f
Revises: e9f07ea687b2
Create Date: 2025-11-15 17:00:51.926206

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3e19cea1d04f"
down_revision: Union[str, Sequence[str], None] = "e9f07ea687b2"
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
