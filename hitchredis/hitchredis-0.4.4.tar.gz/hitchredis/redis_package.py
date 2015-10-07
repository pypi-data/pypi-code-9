from hitchtest import HitchPackage, utils
from subprocess import check_output, call
from os.path import join, exists
from os import makedirs, chdir


ISSUES_URL = "http://github.com/hitchtest/hitchredis/issues"

class RedisPackage(HitchPackage):
    VERSIONS = [
        '2.6.14', '2.6.15', '2.6.16', '2.6.17',
        '2.8.0-rc1', '2.8.0-rc2','2.8.0-rc3', '2.8.0-rc4', '2.8.0-rc5', '2.8.0-rc6',
        '2.8.0', '2.8.1', '2.8.2', '2.8.3', '2.8.4', '2.8.5',
        '2.8.6', '2.8.7', '2.8.8', '2.8.9', '2.8.10',
        '2.8.11', '2.8.12', '2.8.13', '2.8.14', '2.8.15',
        '2.8.16', '2.8.17', '2.8.18', '2.8.19', '2.8.20', '2.8.21',
        '3.0.0-rc1', '3.0.0', '3.0.1', '3.0.2', '3.0.3', '3.0.4',
    ]

    name = "Redis"

    def __init__(self, version, directory=None, bin_directory=None):
        super(RedisPackage, self).__init__()
        self.version = self.check_version(version, self.VERSIONS, ISSUES_URL)

        if directory is None:
            self.directory = join(self.get_build_directory(), "redis-{}".format(self.version))
        else:
            self.directory = directory
        self.bin_directory = bin_directory

    def verify(self):
        version_output = check_output([self.server, "--version"]).decode('utf8')
        if self.version not in version_output:
            raise HitchException("Redis version needed is {}, output is: {}.".format(self.version, version_output))

    def build(self):
        download_to = join(self.get_downloads_directory(), "redis-{}.tar.gz".format(self.version))
        utils.download_file(download_to, "http://download.redis.io/releases/redis-{}.tar.gz".format(self.version))
        if not exists(self.directory):
            makedirs(self.directory)
            utils.extract_archive(download_to, self.directory)
            chdir(join(self.directory, "redis-{}".format(self.version)))
            call(["make"])
        self.bin_directory = join(self.directory, "redis-{}".format(self.version), "src")

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
