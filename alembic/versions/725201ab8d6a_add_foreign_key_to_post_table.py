"""add foreign key to post table

Revision ID: 725201ab8d6a
Revises: 15819c47499f
Create Date: 2024-04-25 11:06:58.191420

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '725201ab8d6a'
down_revision: Union[str, None] = '15819c47499f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key(constraint_name='posts_user_fkey',source_table='posts',referent_table='users',
                          local_cols=['owner_id'],remote_cols=['id'],ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fkey','posts')
    op.drop_column('posts','owner_id')
    pass
