# pylint: disable=c0111
try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass
import os
import io


def read_contents(fname='README'):
    return io.open(os.path.join(os.path.dirname(__file__),
                                fname), encoding="utf-8").read()

# If installing this package from git, make sure to include 'gitversion' in
# requirements.txt
from setuptools import setup, find_packages
from version import __VERSION__

setup(
    name='netshow-core',
    version=__VERSION__,
    url="http://github.com/CumulusNetworks/netshow-core",
    description="Linux Network Troubleshooting Tool",
    long_description=read_contents(),
    author='Cumulus Networks',
    author_email='ce-ceng@cumulusnetworks.com',
    packages=find_packages(),
    namespace_packages=['netshow'],
    install_requires=[
        'setuptools',
        "netshow-core-lib"
    ],
    zip_safe=False,
    scripts=['bin/netshow'],
    data_files=[('share/bash-completion/completions/',
                ['data/completion/netshow']),
                ('share/man/man1/',
                 ['data/man/man1/netshow.1'])],
    license='GPLv2',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: System :: Networking',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: Linux'
    ],
)
