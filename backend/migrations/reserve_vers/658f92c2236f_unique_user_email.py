"""Unique user email

Revision ID: 658f92c2236f
Revises: 2c721c6a16e7
Create Date: 2019-07-15 14:54:18.425328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '658f92c2236f'
down_revision = '2c721c6a16e7'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(table_name='users', column_name='email', nullable=False)
    op.create_unique_constraint('uq_user_email', 'users', ['email'])


def downgrade():
    op.drop_constraint('uq_user_email', 'users')
