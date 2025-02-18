"""create posts table

Revision ID: fd7238dc8c09
Revises: 
Create Date: 2025-02-18 21:48:50.090642

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd7238dc8c09'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('posts',sa.Column('id',sa.Integer(),primary_key=True,nullable=False),
                    sa.Column('title',sa.String(),nullable=False))
    


def downgrade():
    op.drop_table('posts')
    
