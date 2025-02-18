"""add few last columns to posts table

Revision ID: 7076959908a0
Revises: 84e77c7147a1
Create Date: 2025-02-18 22:39:32.496660

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7076959908a0'
down_revision: Union[str, None] = '84e77c7147a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column('published',sa.Boolean(),nullable=False,server_default='True'))
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'),nullable=False))


def downgrade() -> None:
    op.drop_column("posts",'published')
    op.drop_column("posts",'created_at')
