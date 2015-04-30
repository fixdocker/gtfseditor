"""add stop_id constraint to stop_seq

Revision ID: 42debc8b5637
Revises: 5104c2e527c3
Create Date: 2015-04-29 11:20:37.608220

"""

# revision identifiers, used by Alembic.
revision = '42debc8b5637'
down_revision = '5104c2e527c3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'stop_seq', 'stops', ['stop_id'], ['stop_id'],
    	onupdate="CASCADE", ondelete="CASCADE")
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'stop_seq', type_='foreignkey')
    ### end Alembic commands ###
