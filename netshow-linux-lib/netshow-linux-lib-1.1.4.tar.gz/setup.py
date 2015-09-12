# pylint: disable=c0111
# if installing this package from git, make sure to include 'gitversion'
# in requirements.txt
from version import __VERSION__
import os
try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass
from distutils.command.build import build
from setuptools import setup, find_packages
import io


def read_contents(fname='README'):
    """read contents of readme into setup.py long_description field
    """
    return io.open(os.path.join(os.path.dirname(__file__),
                                fname), encoding="utf-8").read()


class BuildWithI18n(build):
    sub_commands = build.sub_commands + [('build_i18n', None)]

    def run(self):
        build.run(self)

setup(
    name='netshow-linux-lib',
    version=__VERSION__,
    url="http://github.com/CumulusNetworks/netshow-linux-lib",
    description="Netshow Provider for Linux Operating Systems",
    author='Cumulus Networks',
    author_email='ce-ceng@cumulusnetworks.com',
    long_description=read_contents(),
    packages=find_packages(),
    zip_safe=False,
    license='GPLv2',
    cmdclass={"build": BuildWithI18n},
    namespace_packages=['netshowlib', 'netshowlib.linux',
                        'netshow', 'netshow.linux'],
    install_requires=[
        'setuptools',
        'netshow-core-lib',
        'netshow-core',
        'network-docopt',
        'tabulate',
        'inflection'
    ],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Development Status :: 4 - Beta',
        'Topic :: System :: Networking',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: Linux'
    ],
    data_files=[('share/netshow-lib/providers', ['data/provider/linux'])],
)
