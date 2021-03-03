"""Create users table

Revision ID: 802705952d35
Revises: 
Create Date: 2019-07-15 11:49:00.802822

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '802705952d35'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('email', sa.String(50), nullable=False),
        sa.Column('google_id', sa.String(30), nullable=True, unique=True),
    )


def downgrade():
    op.drop_table('users')
