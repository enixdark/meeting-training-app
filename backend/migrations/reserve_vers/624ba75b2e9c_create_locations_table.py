"""Create locations  table

Revision ID: 624ba75b2e9c
Revises: f6bb8aa61281
Create Date: 2019-07-15 14:34:29.348005

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '624ba75b2e9c'
down_revision = 'f6bb8aa61281'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'locations',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(30), nullable=False, unique=True),
        sa.Column('is_multi_access', sa.Boolean, nullable=False),
        sa.Column('opened_time', sa.Time, nullable=False),
        sa.Column('closed_time', sa.Time, nullable=False),
        sa.Column('address', sa.String(50), nullable=False, unique=True),
        sa.Column('google_map_id', sa.String(50), nullable=True)
    )


def downgrade():
    op.drop_table('locations')
