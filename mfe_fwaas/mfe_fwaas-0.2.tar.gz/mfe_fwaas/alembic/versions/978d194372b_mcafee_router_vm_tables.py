"""mcafee router vm tables

Revision ID: 978d194372b
Revises: None
Create Date: 2015-08-19 06:02:35.875588

"""

# revision identifiers, used by Alembic.
revision = '978d194372b'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'mfeinterfaceidmap',
        sa.Column('router_id', sa.String(length=36), nullable=False),
        sa.Column('router_port', sa.String(length=36), nullable=False),
        sa.Column('ngfw_port', sa.String(length=36), nullable=False),
        sa.Column('interface_id', sa.Integer, nullable=False),
        sa.PrimaryKeyConstraint('ngfw_port'))

    op.create_table(
        'mferouterportmap',
        sa.Column('router_id', sa.String(length=36), nullable=False),
        sa.Column('interface_id', sa.Integer, nullable=False),
        sa.PrimaryKeyConstraint('router_id'))

def downgrade():
    op.drop_table('mfeinterfaceidmap')
    op.drop_table('mferouterportmap')
