"""Update cascade to user role table

Revision ID: d84f5a79c3d9
Revises: 5badb023e073
Create Date: 2019-08-12 11:23:29.533036

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd84f5a79c3d9'
down_revision = '5badb023e073'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('role_user_role_id_fkey', 'role_user', type_='foreignkey')
    op.drop_constraint('role_user_user_id_fkey', 'role_user', type_='foreignkey')
    op.create_foreign_key(None, 'role_user', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'role_user', 'role', ['role_id'], ['id'], ondelete='CASCADE')


def downgrade():
    op.drop_constraint('role_user_user_id_fkey', 'role_user', type_='foreignkey')
    op.drop_constraint('role_user_role_id_fkey', 'role_user', type_='foreignkey')
    op.create_foreign_key('role_user_user_id_fkey', 'role_user', 'user', ['user_id'], ['id'])
    op.create_foreign_key('role_user_role_id_fkey', 'role_user', 'role', ['role_id'], ['id'])
