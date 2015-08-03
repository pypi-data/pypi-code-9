#!/usr/bin/env python

from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys

_PY3 = sys.version_info[0] == 3


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
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)


def linelist(text):
    """
    Returns each non-blank line in text enclosed in a list.
    """
    return [l.strip() for l in text.strip().splitlines() if l.strip()]

    # The double-mention of l.strip() is yet another fine example of why
    # Python needs en passant aliasing.


def getmetadata(filepath):
    """
    Return a dictionary of metadata from a file, without importing it. This
    trick needed because importing can set off ImportError, in that setup.py
    runs by definition before the modules it sets up (or their dependencies) are
    available.
    """
    if _PY3:
        exec(open(filepath).read())
        return vars()
    else:
        execfile(filepath)
        return locals()

metadata = getmetadata('./quoter/version.py')


setup(
    name='quoter',
    version=metadata['__version__'],
    author='Jonathan Eunice',
    author_email='jonathan.eunice@gmail.com',
    description="Simple, systematic way to quote and wrap text",
    long_description=open('README.rst').read(),
    url='https://bitbucket.org/jeunice/quoter',
    license='Apache License 2.0',
    packages=['quoter'],
    install_requires=['six>=1.9', 'options>=1.2'],
    tests_require=['tox', 'pytest', 'six>=1.9'],
    test_suite="test",
    cmdclass={'test': Tox},
    zip_safe=False,  # it really is, but this will prevent weirdness
    keywords='quote wrap prefix suffix endcap repr represntation html xml',
    classifiers=linelist("""
        Development Status :: 4 - Beta
        Operating System :: OS Independent
        License :: OSI Approved :: Apache Software License
        Intended Audience :: Developers
        Programming Language :: Python
        Programming Language :: Python :: 2
        Programming Language :: Python :: 2.6
        Programming Language :: Python :: 2.7
        Programming Language :: Python :: 3
        Programming Language :: Python :: 3.2
        Programming Language :: Python :: 3.3
        Programming Language :: Python :: 3.4
        Programming Language :: Python :: 3.5
        Programming Language :: Python :: Implementation :: CPython
        Programming Language :: Python :: Implementation :: PyPy
        Topic :: Software Development :: Libraries :: Python Modules
        Topic :: Text Processing :: Filters
        Topic :: Text Processing :: Markup
        Topic :: Text Processing :: Markup :: HTML
        Topic :: Text Processing :: Markup :: XML
    """)
)
