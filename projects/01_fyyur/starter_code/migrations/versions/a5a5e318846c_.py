"""empty message

Revision ID: a5a5e318846c
Revises: f070dfa04cbf
Create Date: 2021-06-22 00:32:33.757092

"""
from datetime import datetime
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5a5e318846c'
down_revision = 'f070dfa04cbf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'venues',
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )
    op.add_column(
        'artists',
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    venues = sa.sql.table('venues', sa.sql.column('created_at'))
    artists = sa.sql.table('artists', sa.sql.column('created_at'))

    now = datetime.now()
    op.execute(
        artists
        .update()
        .where(artists.columns.created_at == sa.sql.null())
        .values(created_at=now)
    )
    op.execute(
        venues
        .update()
        .where(venues.columns.created_at == sa.sql.null())
        .values(created_at=now)
    )

    op.alter_column('venues', 'created_at', nullable=False)
    op.alter_column('artists', 'created_at', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venues', 'created_at')
    op.drop_column('artists', 'created_at')
    # ### end Alembic commands ###
