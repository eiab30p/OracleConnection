"""empty message

Revision ID: 1e449189a500
Revises: a1a628613df9
Create Date: 2018-06-12 11:52:10.909147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e449189a500'
down_revision = 'a1a628613df9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('auth_user', sa.Column('current_login_at', sa.DateTime(), nullable=True))
    op.add_column('auth_user', sa.Column('login_count', sa.Integer(), nullable=True))
    op.alter_column('auth_user', 'active',
               existing_type=sa.INTEGER(),
               type_=sa.Boolean(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('auth_user', 'active',
               existing_type=sa.Boolean(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.drop_column('auth_user', 'login_count')
    op.drop_column('auth_user', 'current_login_at')
    # ### end Alembic commands ###
