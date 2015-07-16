from hitchtest import HitchPackage, utils
from subprocess import check_output
from os.path import join

class RedisPackage(HitchPackage):
    POSTGRES_VERSIONS = []

    def __init__(self, version, directory=None, bin_directory=None):
        self.version = version
        self.directory = directory
        self.bin_directory = bin_directory

    def verify(self):
        version_output = check_output([self.server, "--version"]).decode('utf8')
        if self.version not in version_output:
            raise HitchException("Redis version needed is {}, output is: {}.".format(self.version, version_output))

    def build(self):
        raise NotImplementedError("Redis cannot be build from scratch yet.")

    @property
    def server(self):
        if self.bin_directory is None:
            raise RuntimeError("bin_directory not set.")
        return join(self.bin_directory, "redis-server")

    @property
    def cli(self):
        if self.bin_directory is None:
            raise RuntimeError("bin_directory not set.")
        return join(self.bin_directory, "redis-cli")
