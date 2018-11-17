"""add translation field

Revision ID: 62e364e2879a
Revises: b8696f5566ab
Create Date: 2018-11-17 21:50:31.327170

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62e364e2879a'
down_revision = 'b8696f5566ab'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('event', sa.Column('translation', sa.Boolean(), nullable=True))
    op.execute('UPDATE "event" SET translation=FALSE')
    op.alter_column('event', 'translation', nullable=False)
    op.create_unique_constraint('conference_event_uniqe', 'event', ['conference_id', 'event_id'])


def downgrade():
    op.drop_constraint('conference_event_uniqe', 'event', type_='unique')
    op.drop_column('event', 'translation')
