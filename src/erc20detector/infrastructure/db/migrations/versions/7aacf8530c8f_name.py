"""name

Revision ID: 7aacf8530c8f
Revises: cdf73b1465d8
Create Date: 2024-06-17 12:08:11.498796

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7aacf8530c8f'
down_revision: Union[str, None] = 'cdf73b1465d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contract', sa.Column('contract_name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('contract', 'contract_name')
    # ### end Alembic commands ###
