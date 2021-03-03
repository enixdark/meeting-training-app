"""Add coordionator column to meeting_user table

Revision ID: d330b656efcf
Revises: 082c9ca8bc42
Create Date: 2019-07-16 10:37:53.291882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd330b656efcf'
down_revision = '082c9ca8bc42'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column(table_name='role_user', column_name='is_coordinator')
    op.add_column('meeting_user', sa.Column('is_coordinator', sa.Boolean, nullable=False))


def downgrade():
    op.drop_column(table_name='meeting_user', column_name='is_coordinator')
