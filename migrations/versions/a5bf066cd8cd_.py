"""empty message

Revision ID: a5bf066cd8cd
Revises: None
Create Date: 2022-01-03 00:46:06.151530

"""

# revision identifiers, used by Alembic.
revision = 'a5bf066cd8cd'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Movie_List')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Movie_List',
    sa.Column('movie_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('actor_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['actor_id'], ['actor.id'], name='Movie_List_actor_id_fkey'),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], name='Movie_List_movie_id_fkey'),
    sa.PrimaryKeyConstraint('movie_id', 'actor_id', name='Movie_List_pkey')
    )
    # ### end Alembic commands ###