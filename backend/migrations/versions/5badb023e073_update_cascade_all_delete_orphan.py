"""Update cascade All Delete-orphan

Revision ID: 5badb023e073
Revises: decd3d385f85
Create Date: 2019-08-12 11:21:31.976625

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5badb023e073'
down_revision = 'decd3d385f85'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('meeting_location_id_fkey', 'meeting', type_='foreignkey')
    op.drop_constraint('meeting_creator_id_fkey', 'meeting', type_='foreignkey')
    op.create_foreign_key('meeting_location_id_fkey', 'meeting', 'user', ['creator_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('meeting_creator_id_fkey', 'meeting', 'location', ['location_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('meeting_user_meeting_id_fkey', 'meeting_user', type_='foreignkey')
    op.drop_constraint('meeting_user_user_id_fkey', 'meeting_user', type_='foreignkey')
    op.create_foreign_key('meeting_user_user_id_fkey', 'meeting_user', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('meeting_user_meeting_id_fkey', 'meeting_user', 'meeting', ['meeting_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('meeting_user_meeting_id_fkey', 'meeting_user', type_='foreignkey')
    op.drop_constraint('meeting_user_user_id_fkey', 'meeting_user', type_='foreignkey')
    op.create_foreign_key('meeting_user_user_id_fkey', 'meeting_user', 'user', ['user_id'], ['id'])
    op.create_foreign_key('meeting_user_meeting_id_fkey', 'meeting_user', 'meeting', ['meeting_id'], ['id'])
    op.drop_constraint('meeting_creator_id_fkey', 'meeting', type_='foreignkey')
    op.drop_constraint('meeting_location_id_fkey', 'meeting', type_='foreignkey')
    op.create_foreign_key('meeting_creator_id_fkey', 'meeting', 'user', ['creator_id'], ['id'])
    op.create_foreign_key('meeting_location_id_fkey', 'meeting', 'location', ['location_id'], ['id'])
    # ### end Alembic commands ###
