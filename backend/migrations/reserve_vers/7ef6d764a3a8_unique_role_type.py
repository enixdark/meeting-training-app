"""Unique role type

Revision ID: 7ef6d764a3a8
Revises: 658f92c2236f
Create Date: 2019-07-15 15:30:26.750125

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ef6d764a3a8'
down_revision = '658f92c2236f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint('uq_role_type', 'roles', ['role_type'])


def downgrade():
    op.drop_constraint('uq_role_type', 'roles')
