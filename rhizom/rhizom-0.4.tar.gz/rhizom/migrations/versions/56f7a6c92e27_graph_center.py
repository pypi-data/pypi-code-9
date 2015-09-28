"""Graph center

Revision ID: 56f7a6c92e27
Revises: 947e4289885
Create Date: 2015-09-19 17:33:15.800980

"""

# revision identifiers, used by Alembic.
revision = '56f7a6c92e27'
down_revision = '947e4289885'
branch_labels = None
depends_on = None

import sqlalchemy as sa
from alembic import op
from rhizom.database import is_sqlite, exists_in_db


# don't import the table definition from the models, it may break this
# migration when the model is updated in the future (see the Alembic doc)
graph_table = sa.sql.table('graphs',
    sa.sql.column('id', sa.Integer),
    sa.sql.column('center_id', sa.Integer),
    )
person_table = sa.sql.table('persons',
    sa.sql.column('id', sa.Integer),
    sa.sql.column('graph_id', sa.Integer),
    sa.sql.column('center', sa.Boolean),
    )

def upgrade():
    op.add_column('graphs', sa.Column('center_id', sa.Integer(), nullable=True))
    connection = op.get_bind()
    if not is_sqlite(connection):
        op.create_foreign_key(None, 'graphs', 'persons', ['center_id'], ['id'])

    # Now migrate the data.
    for graph in connection.execute(graph_table.select()).fetchall():
        graph_id = graph["id"]
        center = connection.execute(person_table.select().where(sa.and_(
            person_table.c.graph_id == graph_id,
            person_table.c.center == True))).fetchone()
        if center:
            connection.execute(graph_table.update().where(
                graph_table.c.id == graph_id).values(
                center_id=center["id"]))

    if not is_sqlite(connection):
        op.drop_column('persons', 'center')


def downgrade():
    connection = op.get_bind()

    if not exists_in_db(connection, 'persons', 'center'):
        op.add_column('persons', sa.Column('center', sa.BOOLEAN(),
            server_default=sa.sql.expression.false(),
            autoincrement=False, nullable=False))

    # Now migrate the data.
    for graph in connection.execute(graph_table.select()).fetchall():
        if not graph["center_id"]:
            continue
        connection.execute(person_table.update().where(sa.and_(
            person_table.c.graph_id == graph["id"],
            person_table.c.id == graph["center_id"])).values(
            center=True))

    if not is_sqlite(connection):
        op.drop_constraint(None, 'graphs', type_='foreignkey')
        op.drop_column('graphs', 'center_id')
