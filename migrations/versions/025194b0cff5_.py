"""add rendered url to event

Revision ID: 025194b0cff5
Revises: 
Create Date: 2018-10-31 23:20:49.635033

"""
from alembic import op
import sqlalchemy as sa

revision = '025194b0cff5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('event', sa.Column('rendered_url', sa.Unicode(length=512), nullable=True))

def downgrade():
    op.drop_column('event', 'rendered_url')
