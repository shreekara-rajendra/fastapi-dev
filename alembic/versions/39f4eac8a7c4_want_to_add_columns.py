"""want to add columns

Revision ID: 39f4eac8a7c4
Revises: fc92ca20b27f
Create Date: 2024-04-25 10:08:14.385487

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '39f4eac8a7c4'
down_revision: Union[str, None] = 'fc92ca20b27f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False,primary_key=False))
    pass

def downgrade() -> None:
    op.drop_column('posts','content')
    pass
