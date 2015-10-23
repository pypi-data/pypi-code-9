import sys
import os

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

PKGNAME = 'oydiv_rpc'

# defines VERSION and VERSION_INFO
exec(open(os.path.join(os.path.join(os.path.dirname(__file__), PKGNAME), 'version.py')).read())



# copied from https://testrun.org/tox/latest/example/basic.html#integration-with-setuptools-distribute-test-commands
class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        errno = tox.cmdline(args=shlex.split(self.tox_args))
        sys.exit(errno)


install_requires=[
    'six', 'requests', 'suds-jurko', 'arrow', 'pymysql',
    'py_email_validation',
]

if sys.version_info < (3, 2):
    install_requires.append('functools32')

packages = find_packages(exclude=['tests*'])

setup(
    packages=packages,
    name=PKGNAME,
    version=VERSION,
    py_modules=packages,
    author_email='dev@ajenta.net',
    url='https://github.com/ajenta/oydiv-rpc',
    author='ajenta',
    include_package_data=True,
    install_requires=install_requires,
    tests_require=['tox', 'mock'],
    cmdclass={'test': Tox}
)
