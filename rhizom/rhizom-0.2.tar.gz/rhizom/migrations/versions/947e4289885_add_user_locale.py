"""Add User.locale

Revision ID: 947e4289885
Revises: 
Create Date: 2015-09-01 17:55:27.265099

"""

# revision identifiers, used by Alembic.
revision = '947e4289885'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('users', sa.Column('locale', sa.Unicode(length=10), nullable=True))


def downgrade():
    op.drop_column('users', 'locale')
