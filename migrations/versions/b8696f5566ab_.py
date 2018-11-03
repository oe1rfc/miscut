"""add file constraint

Revision ID: b8696f5566ab
Revises: 025194b0cff5
Create Date: 2018-11-03 20:44:58.548793

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8696f5566ab'
down_revision = '025194b0cff5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint('file_uniqe', 'video_file', ['storage_url', 'file_url'])


def downgrade():
    op.drop_constraint('file_uniqe', 'video_file', type_='unique')
