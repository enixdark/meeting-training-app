"""Create meetings table

Revision ID: cc45857d732a
Revises: 624ba75b2e9c
Create Date: 2019-07-15 14:41:15.196133

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc45857d732a'
down_revision = '624ba75b2e9c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'meetings',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('creator_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('is_periodic', sa.Boolean, nullable=False),
        sa.Column('state', sa.Boolean, nullable=False),
        sa.Column('location_id', sa.Integer, sa.ForeignKey('locations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('started_time', sa.DateTime, nullable=False),
        sa.Column('finished_time', sa.DateTime, nullable=False),
    )


def downgrade():
    op.drop_table('meetings')
