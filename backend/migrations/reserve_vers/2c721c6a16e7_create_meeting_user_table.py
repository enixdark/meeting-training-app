"""Create meeting user table

Revision ID: 2c721c6a16e7
Revises: cc45857d732a
Create Date: 2019-07-15 14:51:25.995873

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2c721c6a16e7'
down_revision = 'cc45857d732a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'meeting_user',
        sa.Column('meeting_id', sa.Integer, sa.ForeignKey('meetings.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('is_accepted', sa.Boolean, nullable=False)
    )


def downgrade():
    op.drop_table('meeting_user')
