from hitchtest import HitchPackage, utils
from subprocess import check_output, call
from hitchtest.environment import checks
from os.path import join, exists
from os import makedirs, chdir


ISSUES_URL = "http://github.com/hitchtest/hitchmemcache/issues"


class MemcachePackage(HitchPackage):
    VERSIONS = [
        "1.4.24", "1.4.23", "1.4.22", "1.4.21", "1.4.20",
        "1.4.19", "1.4.18", "1.4.17", "1.4.16",
    ]

    LIBEVENT_VERSIONS = [
        u'2.1.5-beta', u'2.1.4-alpha', u'2.1.3-alpha', u'2.1.2-alpha', u'2.1.1-alpha',
        u'2.0.22-stable', u'2.0.21-stable', u'2.0.20-stable', u'2.0.19-stable', u'2.0.18-stable',
        u'2.0.17-stable', u'2.0.16-stable', u'2.0.15-stable', u'2.0.14-stable', u'2.0.13-stable',
        u'2.0.12-stable', u'2.0.11-stable', u'2.0.10-stable',
        u'2.0.8-rc', u'2.0.7-rc', u'2.0.6-rc', u'2.0.5-beta'
    ]

    name = "Memcache"

    def __init__(self, version, libevent_version="2.0.22-stable", bin_directory=None):
        super(MemcachePackage, self).__init__()
        self.version = self.check_version(version, self.VERSIONS, ISSUES_URL)
        self.libevent_version = self.check_version(libevent_version, self.LIBEVENT_VERSIONS, ISSUES_URL)
        self.libevent_directory = join(self.get_build_directory(), "memcache-libevent-{}".format(self.libevent_version))
        self.directory = join(self.get_build_directory(), "memcache-{}-with-libevent-{}".format(self.version, self.libevent_version))
        self.bin_directory = bin_directory
        checks.packages(["build-essential", ])

    def verify(self):
        version_output = check_output([self.memcached, "-V"]).decode('utf8')
        if self.version not in version_output:
            raise HitchException("Memcache version needed is {}, output is: {}.".format(self.version, version_output))

    def build_libevent(self):
        download_to = join(self.get_downloads_directory(), "libevent-{}.tar.gz".format(self.libevent_version))
        download_url = "https://github.com/libevent/libevent/releases/download/release-{0}/libevent-{0}.tar.gz".format(self.libevent_version)
        utils.download_file(download_to, download_url)
        if not exists(self.libevent_directory):
            makedirs(self.libevent_directory)
            utils.extract_archive(download_to, self.libevent_directory)
            full_directory = join(self.libevent_directory, "libevent-{}".format(self.libevent_version))
            chdir(full_directory)
            call(["./configure", "--prefix={}".format(full_directory)])
            call(["make"])
        self.libevent_path = join(self.libevent_directory, "lib")


    def build(self):
        self.build_libevent()
        download_to = join(self.get_downloads_directory(), "memcache-{}.tar.gz".format(self.version))
        download_url = "http://www.memcached.org/files/memcached-{}.tar.gz".format(self.version)
        utils.download_file(download_to, download_url)
        if not exists(self.directory):
            makedirs(self.directory)
            utils.extract_archive(download_to, self.directory)
            full_directory = join(self.directory, "memcached-{}".format(self.version))
            chdir(full_directory)
            call(["./configure", "--prefix={}".format(full_directory), "--with-libevent={}".format(self.libevent_path)])
            call(["make"])
            call(["make", "install"])
        self.bin_directory = join(self.directory, "memcached-{}".format(self.version))

    @property
    def memcached(self):
        if self.bin_directory is None:
            raise RuntimeError("bin_directory not set.")
        return join(self.bin_directory, "memcached")
