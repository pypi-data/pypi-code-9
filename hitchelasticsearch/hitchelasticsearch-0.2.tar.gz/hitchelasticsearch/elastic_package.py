from hitchtest import HitchPackage, utils
from subprocess import check_output, call
from hitchtest.environment import checks
from os.path import join, exists
from os import makedirs, chdir


ISSUES_URL = "http://github.com/hitchtest/hitchelasticsearch/issues"

class ElasticPackage(HitchPackage):
    VERSIONS = [
        '1.7.1', '1.7.0',
        '1.6.2', '1.6.1', '1.6.0',
        '1.5.2', '1.5.1', '1.5.0',
        '1.4.5', '1.4.4', '1.4.3', '1.4.2', '1.4.1', '1.4.0.Beta1', '1.4.0',
        '1.3.9', '1.3.8', '1.3.7', '1.3.6', '1.3.5', '1.3.4', '1.3.3', '1.3.2', '1.3.1', '1.3.0',
        '1.2.4', '1.2.3', '1.2.2', '1.2.1', '1.2.0',
    ]

    name = "ElasticSearch"

    def __init__(self, version, directory=None, bin_directory=None):
        super(ElasticPackage, self).__init__()
        self.version = self.check_version(version, self.VERSIONS, ISSUES_URL)

        checks.packages(["openjdk-7-jre", ])

        if directory is None:
            self.directory = join(self.get_build_directory(), "elasticsearch-{}".format(self.version))
        else:
            self.directory = directory
        self.bin_directory = bin_directory

    def verify(self):
        raise RuntimeError(
            "Elastic search does not implement a --version parameter."
            " Raise an issue at http://github.com/elastic/elasticsearch"
        )

    def build(self):
        download_url = "https://download.elastic.co/elasticsearch/elasticsearch/elasticsearch-{}.tar.gz".format(
            self.version,
        )
        utils.download_file(join(self.get_downloads_directory(), "elasticsearch-{}.tar.gz".format(self.version)), download_url)
        if not exists(self.directory):
            utils.extract_archive(
                join(self.get_build_directory(), "elasticsearch-{}.tar.gz".format(self.version)),
                self.get_build_directory()
            )
        self.bin_directory = join(self.directory, "bin")

    @property
    def elasticsearch(self):
        if self.bin_directory is None:
            raise RuntimeError("bin_directory not set.")
        return join(self.bin_directory, "elasticsearch")

