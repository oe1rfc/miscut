"""add schedulexml to database

Revision ID: 301863defd4f
Revises: 62e364e2879a
Create Date: 2018-11-21 22:54:04.125096

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '301863defd4f'
down_revision = '62e364e2879a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('conference', sa.Column('schedulexml', sa.UnicodeText(), nullable=True))


def downgrade():
    op.drop_column('conference', 'schedulexml')
