from hitchtest import HitchPackage, utils
from subprocess import check_output
from os.path import join

class PostgresPackage(HitchPackage):
    POSTGRES_VERSIONS = []

    def __init__(self, version="9.4.2", directory=None, bin_directory=None):
        self.version = version
        self.directory = directory
        self.bin_directory = bin_directory

    def verify(self):
        version_output = check_output([self.postgres, "--version"]).decode('utf8')
        if self.version not in version_output:
            raise RuntimeError("Postgres version needed is {}, output is: {}.".format(self.version, version_output))

    def build(self):
        raise NotImplementedError("Postgres cannot be build from scratch yet.")

    @property
    def initdb(self):
        if self.bin_directory is None:
            raise RuntimeError("bin_directory not set.")
        return join(self.bin_directory, "initdb")

    @property
    def postgres(self):
        if self.bin_directory is None:
            raise RuntimeError("bin_directory not set.")
        return join(self.bin_directory, "postgres")

    @property
    def psql(self):
        if self.bin_directory is None:
            raise RuntimeError("bin_directory not set.")
        return join(self.bin_directory, "psql")

    @property
    def pg_dump(self):
        if self.bin_directory is None:
            raise RuntimeError("bin_directory not set.")
        return join(self.bin_directory, "pg_dump")

    @property
    def pg_restore(self):
        if self.bin_directory is None:
            raise RuntimeError("bin_directory not set.")
        return join(self.bin_directory, "pg_restore")
