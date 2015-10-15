import psycopg2
import os

from psycopg2._psycopg import ProgrammingError
try:
    from urllib.parse import urlsplit
except ImportError:  # pragma: no cover
    from urlparse import urlsplit


DEFAULT_GROUP = {'default': './migrations/'}
STATUS_PENDING = -1
STATUS_PARTIAL = 0
STATUS_OK = 1

SELECT_SQL = 'select group_name, name from migration_history'
INSERT_SQL = 'insert into migration_history values (%s, %s)'
CREATE_TABLE_DDL = '''
BEGIN;
CREATE TABLE migration_history (
  group_name TEXT NOT NULL,
  name TEXT NOT NULL,
  PRIMARY KEY (group_name, name)
);
END;
'''


class MigrationController(object):

    def __init__(self, databases=None, groups=None):
        self._databases = databases or {}
        self._groups = groups or DEFAULT_GROUP
        self._connections = dict()
        self._completed = self.list_completed()

    def list_completed(self):
        return {
            db: self.list_completed_in_db(db)
            for db in self._databases.keys()
        }

    def list_completed_in_db(self, db):
        cur = self.get_cursor(db)
        completed = {}

        try:
            cur.execute(SELECT_SQL)
            for group, name in cur.fetchall() or []:
                if group not in completed:
                    completed[group] = []

                completed[group].append(name)
        except ProgrammingError:
            # Must rollback previous transaction
            cur.execute('ROLLBACK;')
            cur.execute(CREATE_TABLE_DDL)
        cur.close()

        return completed

    def list(self):
        return {
            k: self.list_group(k, f) for k, f in (self._groups or {}).items()
        }

    def list_group(self, group, folder):
        return [
            self.migration_info(group, migration)
            for migration in os.listdir(folder)
            if os.path.isdir(os.path.join(folder, migration))
        ]

    def migrate(self):
        for group, migrations in self.list().items():
            for migration in migrations:
                for db, status in migration['status']['databases'].items():
                    if not status:
                        script = os.path.join(
                            self._groups.get(group),
                            migration['name'],
                            'forward.sql'
                        )
                        with open(script) as f:
                            cur = self.get_cursor(db)
                            cur.execute('BEGIN;')
                            cur.execute(f.read())
                            cur.execute(
                                INSERT_SQL,
                                (group, migration['name'])
                            )
                            cur.execute('END;')

    def migration_info(self, group, migration_name):
        return dict(
            name=migration_name,
            group=group,
            status=self.migration_status(group, migration_name)
        )

    def migration_status(self, group, migration_name):
        db_status = {
            db: self.is_migration_applied(group, migration_name, db)
            for db in (self._databases or {}).keys()
        }

        return dict(
            databases=db_status,
            all=STATUS_OK if False not in db_status.values() else
            STATUS_PARTIAL if True in db_status.values() else
            STATUS_PENDING
        )

    def is_migration_applied(self, group, migration, db):
        return migration in (self._completed or {}).get(db, {}).get(group, [])

    def get_cursor(self, db):
        return self.get_conn(db).cursor()

    def get_conn(self, db):
        if db not in self._connections:
            self._connections[db] = psycopg2.connect(
                **self.parse_pgurl(self._databases[db])
            )

        return self._connections[db]

    def parse_pgurl(self, url):
        """
        Given a Postgres url, return a dict with keys for user, password,
        host, port, and database.
        """
        parsed = urlsplit(url)

        return {
            'user': parsed.username,
            'password': parsed.password,
            'database': parsed.path.lstrip('/'),
            'host': parsed.hostname,
            'port': parsed.port,
        }

    def close(self):
        for conn in self._connections.values():
            conn.close()
