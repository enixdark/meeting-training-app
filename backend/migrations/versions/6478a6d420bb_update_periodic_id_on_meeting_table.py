"""update_periodic_id_on_meeting_table

Revision ID: 6478a6d420bb
Revises: 31a2bc07e93a
Create Date: 2019-09-19 14:54:09.150133

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6478a6d420bb'
down_revision = '31a2bc07e93a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('meeting', sa.Column('periodic_id', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('meeting', 'periodic_id')
    # ### end Alembic commands ###