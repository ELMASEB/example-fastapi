"""add foreign keys to posts table

Revision ID: 84e77c7147a1
Revises: 54664d3e0706
Create Date: 2025-02-18 22:28:21.998581

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84e77c7147a1'
down_revision: Union[str, None] = '54664d3e0706'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fk',source_table='posts',referent_table='users',
                          local_cols=['owner_id'],remote_cols=['id'],ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('post_users_fk',table_name='posts')
    op.drop_column('posts','owner_id')
