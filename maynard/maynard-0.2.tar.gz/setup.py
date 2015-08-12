from setuptools import setup, find_packages
import sys

if (sys.version_info.major < 3) or \
    (sys.version_info.major == 3 and sys.version_info.minor < 2):
    sys.exit("Maynard requires Python version 3.1 or newer.")

setup(
    name="maynard",
    version="0.2",
    packages=find_packages(),

    author="Larry Hastings",
    author_email="larry@hastings.org",
    license="zlib",
    url="https://pypi.python.org/pypi/maynard/",
    )
