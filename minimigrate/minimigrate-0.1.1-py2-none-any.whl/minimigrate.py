"""
MiniMigrate: a simple migration tool
"""
from __future__ import print_function
import imp
import logging
import os
import re
import sys

import pathlib
from sqlalchemy import create_engine
from sqlalchemy import text

logging.basicConfig(stream=sys.stderr, format='%(message)s')


class MigrationFile(object):
    """A migration module containing an upgrade and downgrade function"""
    def __init__(self, path, pattern=None):
        self.path = pathlib.Path(path)
        self.pattern = re.compile(pattern)
        self.version = self._get_version()
        self.module = self._get_module()

    def _get_version(self):
        return int(self.pattern.match(self.path.name).group('version'))

    def _get_module(self):
        module_name = self.path.name.replace('.py', '')
        module_path = str(self.path.absolute())
        module = imp.load_source(module_name, module_path)
        return module

    def _invoke(self, method, *args, **kw):
        method = getattr(self.module, method)
        return method(*args, **kw)

    def upgrade(self, *args, **kw):
        self._invoke('upgrade', *args, **kw)

    def downgrade(self, *args, **kw):
        self._invoke('downgrade', *args, **kw)

    def is_valid(self):
        """Migration modules must have an upgrade and a downgrade function"""
        try:
            assert callable(self.module.upgrade)
            assert callable(self.module.downgrade)
        except AssertionError:
            return False
        return True


class Migrations(object):
    """Get migrations and filter them based on current and target versions"""
    def __init__(self, path='migrations', pattern='^v(?P<version>\d+)_.*.py$'):
        self.migrations = self.get_migrations(path, pattern)
        self.versions = sorted(self.migrations.keys())

    def latest_version(self):
        return self.versions[-1]

    def get_migrations(self, path, pattern):
        migrations = {}
        for file_path in os.listdir(path):
            if not re.match(pattern, file_path):
                continue
            abspath = os.path.join(path, file_path);
            migration = MigrationFile(abspath, pattern)
            migrations[migration.version] = migration
        return migrations

    def filtered_migrations(self, current_version, target_version):
        """Figure out which versions need to be executed"""
        try:
            current_index = self.versions.index(current_version)
        except ValueError:
            current_index = 0
        
        target_index = self.versions.index(target_version)
        
        if current_version > target_version:
            # Downgrade
            target_versions = self.versions[current_index : target_index :-1]
            return [self.migrations[version].downgrade for version in target_versions]
        else:
            # Upgrade
            target_versions = self.versions[current_index : target_index + 1]
            return [self.migrations[version].upgrade for version in target_versions]


class Migrator(object):
    """Runs migrations"""
    def __init__(self, database_uri, migrations_path):
        self.engine = create_engine(database_uri)
        self.migrations = Migrations(migrations_path)
        self.schema_version = SchemaVersion(self.engine)

    def migrate(self, target_version=None):        
        if target_version is None:
            target_version = self.migrations.latest_version()
        current_version = self.schema_version.get()

        if target_version == current_version:
            logging.warning('Database version is already at v%s' % target_version)
            return

        migrations = self.migrations.filtered_migrations(current_version, target_version)
        with self.engine.begin() as connection:
            for migrate_method in migrations:
                migrate_method(connection)
            self.schema_version.update(target_version)


class SchemaVersion(object):
    """Read and write the schema version to the database."""
    queries = {
        'create': text('CREATE TABLE schema_info (version int)'),
        'insert': text('INSERT INTO schema_info (version) VALUES (:version)'),
        'select': text('SELECT version FROM schema_info'),
        'update': text('UPDATE schema_info SET version = :version'),
    }
    def __init__(self, engine, table_name='schema_info'):
        self.engine = engine
        if table_name not in engine.table_names():
            self.create()
    
    def create(self):
        self.engine.execute(self.queries['create'])
        self.engine.execute(self.queries['insert'], version=0)

    def get(self):
        results = self.engine.execute(self.queries['select'])
        return results.scalar()

    def update(self, version):
        self.engine.execute(self.queries['update'], version=version)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('database_uri')
    parser.add_argument('migrations_directory')
    parser.add_argument('-v', '--version', default=None, type=int)
    args = parser.parse_args()
    migrator = Migrator(args.database_uri, args.migrations_directory)
    migrator.migrate(args.version)


if __name__ == '__main__':
    main()

