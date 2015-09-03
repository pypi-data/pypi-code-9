from distutils.core import setup
from setuptools import find_packages
from bgdata import __version__, __author__, __author_email__

setup(
    name="bgdata",
    version=__version__,
    packages=find_packages(),
    author=__author__,
    author_email=__author_email__,
    description="Simple data repository managment.",
    license="Apache License 2",
    keywords=["data", "managment", "repository"],
    url="https://bitbucket.org/bgframework/bgdata",
    download_url="https://bitbucket.org/bgframework/bgdata/get/"+__version__+".tar.gz",
    install_requires=[],
    classifiers=[],
    entry_points={
        'console_scripts': [
            'bg-data = bgdata.utils:cmdline',
            'bg-axel = bgdata.pyaxel:cmdline'
        ]
    }
)
