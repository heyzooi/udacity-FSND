"""empty message

Revision ID: 5b361d98a5e6
Revises: a399787daa1e
Create Date: 2021-06-20 15:22:32.691674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b361d98a5e6'
down_revision = 'a399787daa1e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Venue', 'website', new_column_name='website_link')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Venue', 'website_link', new_column_name='website')
    # ### end Alembic commands ###
