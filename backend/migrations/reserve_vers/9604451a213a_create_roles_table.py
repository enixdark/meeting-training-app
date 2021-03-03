"""Create roles table

Revision ID: 9604451a213a
Revises: 802705952d35
Create Date: 2019-07-15 11:55:06.451556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9604451a213a'
down_revision = '802705952d35'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('role_type', sa.String(20), nullable=False)
    )


def downgrade():
    op.drop_table('roles')
