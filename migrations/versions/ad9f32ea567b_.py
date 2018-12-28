"""allow longer schedule urls

Revision ID: ad9f32ea567b
Revises: 301863defd4f
Create Date: 2018-12-28 11:02:04.874482

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad9f32ea567b'
down_revision = '301863defd4f'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('conference', 'scheduleurl',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.Unicode(length=512),
               existing_nullable=True)


def downgrade():
    op.alter_column('conference', 'scheduleurl',
               existing_type=sa.Unicode(length=512),
               type_=sa.VARCHAR(length=64),
               existing_nullable=True)
