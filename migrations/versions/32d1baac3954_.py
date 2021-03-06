"""empty message

Revision ID: 32d1baac3954
Revises: 65f776ede1bf
Create Date: 2019-01-12 10:43:07.006713

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32d1baac3954'
down_revision = '65f776ede1bf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('follow', sa.Column('follower_id', sa.Integer(), nullable=True))
    op.add_column('follow', sa.Column('following_id', sa.Integer(), nullable=True))
    op.drop_constraint(None, 'follow', type_='foreignkey')
    op.drop_constraint(None, 'follow', type_='foreignkey')
    op.create_foreign_key(None, 'follow', 'user', ['follower_id'], ['id'])
    op.create_foreign_key(None, 'follow', 'user', ['following_id'], ['id'])
    op.drop_column('follow', 'follower')
    op.drop_column('follow', 'following')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('follow', sa.Column('following', sa.INTEGER(), nullable=True))
    op.add_column('follow', sa.Column('follower', sa.INTEGER(), nullable=True))
    op.drop_constraint(None, 'follow', type_='foreignkey')
    op.drop_constraint(None, 'follow', type_='foreignkey')
    op.create_foreign_key(None, 'follow', 'user', ['following'], ['id'])
    op.create_foreign_key(None, 'follow', 'user', ['follower'], ['id'])
    op.drop_column('follow', 'following_id')
    op.drop_column('follow', 'follower_id')
    # ### end Alembic commands ###
