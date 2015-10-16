import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

# setup.py test uses pytest
# https://pytest.org/latest/goodpractises.html#integration-with-setuptools-test-commands

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    print('WARNING: cannot convert README.md to README.rst. Using README.md')
    long_description = open('README.md').read()

setup(
    name='qudb',
    author='Ahmad Khayyat',
    author_email='akhayyat@gmail.com',
    url='https://bitbucket.org/akhayyat/qudb',
    version='0.6',
    description='qudb: Question Database',
    long_description=long_description,
    license='BSD',
    packages=['qudb',],
    install_requires=[
        'sqlalchemy',
        'jinja2',
    ],
    extras_require={
        'import_export': ['pyyaml>=3.11'],
    },
    tests_require=['pytest'],
    cmdclass = {'test': PyTest},
    entry_points={
        'console_scripts': ['qm = qudb.qm:main'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Education',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Education',
        'Topic :: Education :: Computer Aided Instruction (CAI)',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],
)
