import sys
import os
from setuptools import setup, Command

# Pull version from source without importing
# since we can't import something we haven't built yet :)
exec(open('mc/ioc/version.py').read())

class Tox(Command):

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    @classmethod
    def run(cls):
        import tox
        sys.exit(tox.cmdline([]))


test_require = ['tox', 'mock']
if sys.version_info < (2, 7):
    test_require.append('unittest2')

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README')) as f:
    README = f.read()

setup(
    name="mc-ioc",
    version=__version__,

    tests_require=test_require,
    cmdclass={"test": Tox},

    packages=[
        "mc",
        "mc.ioc",
    ],

    author="MENA Commerce",
    author_email="accounts@menacommerce.com",
    url="http://menacommerce.com",
    license="Apache License 2.0",
    description="Python IOC Implementation",
    long_description=README,
    keywords="IOC MC",
    install_requires=['six'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
