"""add avatar url to users table

Revision ID: 59dd8594a55e
Revises: d330b656efcf
Create Date: 2019-07-17 15:21:32.771049

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59dd8594a55e'
down_revision = 'd330b656efcf'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('avatar_url', sa.String(100), nullable=False))


def downgrade():
    op.drop_column(table_name='users', column_name='avatar_url')
