"""add foreign-key to posts table

Revision ID: d4f6f57b7ff4
Revises: 57216d4e9478
Create Date: 2025-11-15 18:19:03.787171

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d4f6f57b7ff4"
down_revision: Union[str, Sequence[str], None] = "57216d4e9478"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "post_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["user_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "user_id")
    pass
