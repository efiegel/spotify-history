"""new tracks table

Revision ID: aa163ca72561
Revises: 
Create Date: 2021-03-11 21:07:13.763941

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa163ca72561'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('my_played_tracks',
    sa.Column('song_name', sa.String(length=200), nullable=True),
    sa.Column('artist_name', sa.String(length=200), nullable=True),
    sa.Column('played_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('timestamp', sa.String(length=11), nullable=True),
    sa.PrimaryKeyConstraint('played_at')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('my_played_tracks')
    # ### end Alembic commands ###
