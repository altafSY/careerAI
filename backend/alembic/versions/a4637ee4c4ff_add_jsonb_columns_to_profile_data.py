"""add jsonb columns to profile_data

Revision ID: a4637ee4c4ff
Revises: 3bf133323670
Create Date: 2025-06-23 14:06:09.611985

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4637ee4c4ff'
down_revision: Union[str, None] = '3bf133323670'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('profile_data')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profile_data',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('mobile_number', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('college', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('degree', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('designation', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('company_names', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('skills', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('experience', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('profile_data_user_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('profile_data_pkey'))
    )
    # ### end Alembic commands ###
