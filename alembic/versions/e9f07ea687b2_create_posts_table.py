"""create posts table

Revision ID: e9f07ea687b2
Revises:
Create Date: 2025-11-15 16:49:31.319767

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e9f07ea687b2"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("posts")
    pass
