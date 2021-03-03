"""create user_role table

Revision ID: 227d7972fc56
Revises: 40a51d118d42
Create Date: 2019-07-22 02:30:45.180876

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '227d7972fc56'
down_revision = '40a51d118d42'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'role_user',
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id')),
        sa.Column('role_id', sa.Integer, sa.ForeignKey('role.id'))
    )


def downgrade():
    op.drop_table('role_user')
