from hitchtest.environment import checks
from hitchserve import Service
from os.path import join
import signal
import shutil
import sys



class PostgresDatabase(object):
    def __init__(self, name, owner, dump=None):
        self.name = name
        self.owner = owner
        self.dump = dump

    def psql(self, command=None):
        """Run PSQL command on this database."""
        return self.database_of.psql(command=command, database=self.name)

    def pg_dump(self, filename=None):
        """Dump this database to 'filename'."""
        return self.database_of.pg_dump(filename, database=self.name)

    @property
    def database_of(self):
        return self._database_of

    @database_of.setter
    def database_of(self, value):
        self._database_of = value

class PostgresUser(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

class PostgresService(Service):
    stop_signal = signal.SIGQUIT

    def __init__(self, postgres_package, port=15432, encoding='UTF-8', locale='en_US', pgdata=None, users=None, databases=None, **kwargs):
        #self.version = version
        self.postgres_package = postgres_package
        self.encoding = encoding
        self.locale = locale
        self.port = port
        #self.pg_installation = PostgresInstallation() if None else postgres_installation
        self.users = users
        self.databases = databases
        self.pgdata = pgdata
        checks.freeports([port, ])
        kwargs['log_line_ready_checker'] = lambda line: "database system is ready to accept connections" in line
        super(PostgresService, self).__init__(**kwargs)

    @property
    def databases(self):
        return self._databases

    @databases.setter
    def databases(self, value):
        self._databases = value
        if self.databases is not None:
            for database in self._databases:
                database.database_of = self

    @property
    def pgdata(self):
        if self._pgdata is None:
            return join(self.service_group.hitch_dir.hitch_dir, 'pgdata')
        else:
            return self._pgdata

    @pgdata.setter
    def pgdata(self, value):
        self._pgdata = value

    @Service.command.getter
    def command(self):
        if self._command is None:
            return [self.postgres_package.postgres,
                '-p', str(self.port),
                '-D', self.pgdata,
                '--unix_socket_directories=' + self.pgdata,
                "--log_destination=stderr",]
        else:
            return self._command

    def setup(self):
        #self.log("Checking postgresql version...")
        #version_output = self.subcommand(self.pg_installation.exec_postgres, "--version").run(check_output=True)
        #if self.version not in version_output:
            #raise HitchException("Postgres version needed is {}, output is: {}.".format(self.version, version_output))
        self.log("Initializing postgresql database...")
        shutil.rmtree(self.pgdata, ignore_errors=True)
        # TODO : Put back encoding + locale
        self.subcommand(self.postgres_package.initdb, self.pgdata).run()

    def poststart(self):
        self.log("Creating users and databases...")
        for user in self.users:
            self.psql(
                """create user {} with password '{}';""".format(user.username, user.password)
            ).run()
        for database in self.databases:
            self.psql(
                """create database {} with owner {};""".format(
                    database.name, database.owner.username
                )
            ).run()
            if database.dump is not None:
                self.psql(database=database.name, filename=database.dump).run()

    def psql(self, command=None, database="template1", filename=None):
        """Run PSQL command."""
        return self.subcommand(
            *tuple([
                self.postgres_package.psql,
                "-d", database, "-p", str(self.port), "--host", self.pgdata,
            ] + (
                ["-c", command, ] if command is not None else []
            ) + (
                ["-f", filename, ] if filename is not None else []
            ))
        )

    def pg_dump(self, filename=None, database="template1"):
        """Dump a database."""
        return self.subcommand(
            *tuple([
                self.postgres_package.pg_dump,
                "-d", database, "-p", str(self.port), "--host", self.pgdata,
            ] + (
                ["-f", filename, ] if filename is not None else []
            ))
        )

    def pg_restore(self, filename, database="template1"):
        """Restore a database."""
        return self.subcommand(*tuple([
            self.postgres_package.pg_restore, "-d", database, "-p",
            str(self.port), "--host", self.pgdata, filename
        ]))
