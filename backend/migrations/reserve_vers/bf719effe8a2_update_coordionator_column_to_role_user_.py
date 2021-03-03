"""Update coordionator column to role_user table

Revision ID: bf719effe8a2
Revises: 7ef6d764a3a8
Create Date: 2019-07-16 10:31:22.154864

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf719effe8a2'
down_revision = '7ef6d764a3a8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('role_user', sa.Column('is_coordinator', sa.Boolean, nullable=False))


def downgrade():
    pass
