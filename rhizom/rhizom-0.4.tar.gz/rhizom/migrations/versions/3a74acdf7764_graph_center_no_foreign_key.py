"""Graph.center no foreign key

Revision ID: 3a74acdf7764
Revises: 56f7a6c92e27
Create Date: 2015-09-24 10:09:37.515100

"""

# revision identifiers, used by Alembic.
revision = '3a74acdf7764'
down_revision = '56f7a6c92e27'
branch_labels = None
depends_on = None

import sqlalchemy as sa
from alembic import op
from rhizom.database import is_sqlite, exists_in_db


def upgrade():
    if not is_sqlite(op.get_bind()):
        op.drop_constraint(None, 'graphs', type_='foreignkey')


def downgrade():
    if not is_sqlite(op.get_bind()):
        op.create_foreign_key(None, 'graphs', 'persons', ['center_id'], ['id'])
