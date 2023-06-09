"""first commit

Revision ID: 282e44c4eb7e
Revises: 
Create Date: 2023-03-14 11:26:01.348037

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '282e44c4eb7e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('external_id', sa.String(length=255), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('is_disabled', sa.Boolean(), nullable=True),
    sa.Column('reset_token', sa.String(length=255), nullable=True),
    sa.Column('scopes', sa.String(length=255), nullable=True),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.Column('modified_by_id', sa.Integer(), nullable=True),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['modified_by_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_user_external_id'), 'user', ['external_id'], unique=False)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_external_id'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
