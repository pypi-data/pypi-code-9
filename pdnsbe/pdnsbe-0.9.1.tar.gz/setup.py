import sys
from setuptools import setup


CUR_VERSION = "0.9.1"

base_dir = "python%d.%d" % (sys.version_info[0], sys.version_info[1])

setup(
    name="pdnsbe",
    packages=["pdnsbe"],
    package_dir={"pdnsbe": "%s/pdnsbe" % base_dir},
    version=CUR_VERSION,
    description="""Library to easily implement and run a python PowerDNS socket
                   backend.""",
    author="Tim Lamballais Tessensohn",
    author_email="tim@wimtie.org",
    url="https://github.com/wimtie/pdnsbe",
    download_url="https://github.com/wimtie/pdnsbe/tarball/%s" % CUR_VERSION,
    keywords=["PowerDNS", "backend", "python", "generic", "pluggable"],
    classifiers=[],
)
