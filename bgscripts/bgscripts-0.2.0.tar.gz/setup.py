from setuptools import setup, find_packages
from bgscripts import __version__, __author__, __author_email__

setup(
    name="bgscripts",
    version=__version__,
    packages=find_packages(),
    author=__author__,
    author_email=__author_email__,
    description="Generic python scripts used at Biomedical Genomics group",
    license="Apache License 2",
    keywords="",
    url="https://bitbucket.org/bgframework/bgscripts",
    download_url="https://bitbucket.org/bgframework/bgscripts/get/"+__version__+".tar.gz",
    long_description=__doc__,
    install_requires=[
        'numpy >= 1.9.2',
        'bgdata >= 0.3.0',
        'intervaltree >= 2.1.0',
        'itab >= 0.1.0'
    ],
    entry_points={
        'console_scripts': [
            'bg-randomizer = bgscripts.randomizer:cmdline'
        ]
    }
)
