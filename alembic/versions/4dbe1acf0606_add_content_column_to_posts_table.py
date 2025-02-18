"""add content column to posts table

Revision ID: 4dbe1acf0606
Revises: fd7238dc8c09
Create Date: 2025-02-18 22:04:42.659430

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4dbe1acf0606'
down_revision: Union[str, None] = 'fd7238dc8c09'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))


def downgrade():
    op.drop_column("posts",'content')
