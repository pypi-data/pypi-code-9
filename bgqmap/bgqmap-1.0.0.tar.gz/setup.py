from setuptools import setup, find_packages

__version__ = '1.0.0'
__author__ = 'Jordi Deu-Pons'
__author_email__ = 'jordi.deu@upf.edu'

setup(
    name="bgqmap",
    version=__version__,
    packages=find_packages(),
    install_requires=['drmaa', 'ago'],
    author=__author__,
    author_email=__author_email__,
    description="Bgqmap it's a python library and script to parallelize multiple jobs in a DRMAA compatible cluster.",
    license="Apache License 2",
    keywords="",
    url="https://bitbucket.org/bgframework/bgqmap",
    download_url="https://bitbucket.org/bgframework/bgqmap/get/"+__version__+".tar.gz",
    entry_points={
        'console_scripts': [
            'bg-qmap = bgqmap.qmap:cmdline'
        ]
    }
)
