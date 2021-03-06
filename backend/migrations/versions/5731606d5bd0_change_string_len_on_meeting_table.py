"""Change string len on meeting table

Revision ID: 5731606d5bd0
Revises: d84f5a79c3d9
Create Date: 2019-08-19 09:34:30.124197

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '5731606d5bd0'
down_revision = 'd84f5a79c3d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('location', 'name',
                    existing_type=sa.VARCHAR(length=50),
                    type_=sa.String(length=200),
                    existing_nullable=False)
    op.alter_column('meeting', 'description',
                    existing_type=sa.VARCHAR(length=500),
                    type_=sa.String(length=5000),
                    existing_nullable=False)
    op.alter_column('meeting', 'name',
                    existing_type=sa.VARCHAR(length=50),
                    type_=sa.String(length=200),
                    existing_nullable=False)
    op.alter_column('user', 'email',
                    existing_type=sa.VARCHAR(length=50),
                    type_=sa.String(length=200),
                    existing_nullable=False)
    op.alter_column('user', 'refresh_token',
                    existing_type=sa.VARCHAR(length=100),
                    type_=sa.String(length=200),
                    existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'refresh_token',
                    existing_type=sa.String(length=200),
                    type_=sa.VARCHAR(length=100),
                    existing_nullable=True)
    op.alter_column('user', 'email',
                    existing_type=sa.String(length=200),
                    type_=sa.VARCHAR(length=50),
                    existing_nullable=False)
    op.alter_column('meeting', 'name',
                    existing_type=sa.String(length=200),
                    type_=sa.VARCHAR(length=50),
                    existing_nullable=False)
    op.alter_column('meeting', 'description',
                    existing_type=sa.String(length=5000),
                    type_=sa.VARCHAR(length=500),
                    existing_nullable=False)
    op.alter_column('location', 'name',
                    existing_type=sa.String(length=200),
                    type_=sa.VARCHAR(length=50),
                    existing_nullable=False)
    # ### end Alembic commands ###
