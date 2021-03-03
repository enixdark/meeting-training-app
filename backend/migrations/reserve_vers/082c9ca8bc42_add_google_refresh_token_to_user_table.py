"""Add google refresh token to user table

Revision ID: 082c9ca8bc42
Revises: bf719effe8a2
Create Date: 2019-07-16 10:34:10.652706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '082c9ca8bc42'
down_revision = 'bf719effe8a2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('refresh_token', sa.String(50), nullable=False, unique=True))


def downgrade():
    op.drop_column(table_name='users', column_name='refresh_token')
