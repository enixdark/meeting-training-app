"""Create roleuser table

Revision ID: f6bb8aa61281
Revises: 9604451a213a
Create Date: 2019-07-15 11:57:06.855036

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f6bb8aa61281'
down_revision = '9604451a213a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'role_user',
        sa.Column('role_id', sa.Integer, sa.ForeignKey('roles.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    )


def downgrade():
    op.drop_table('role_user')
