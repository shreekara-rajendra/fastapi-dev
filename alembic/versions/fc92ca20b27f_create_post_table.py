"""create post table

Revision ID: fc92ca20b27f
Revises: 
Create Date: 2024-04-25 09:57:53.922989

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc92ca20b27f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                    sa.Column('title',sa.String(),nullable=False,primary_key=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
