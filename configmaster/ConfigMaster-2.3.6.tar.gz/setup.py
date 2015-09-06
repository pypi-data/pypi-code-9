from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys


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


setup(
    name="ConfigMaster",
    version='2.3.6',
    description="Programmatic configuration library for Python 3.",
    author="Isaac Dickinson",
    author_email="eyesismine@gmail.com",
    url="https://github.com/SunDwarf/ConfigMaster",
    packages=["configmaster"],
    license="MIT",
    tests_require=["pytest",
                   "pytest-cov",
                   "python-coveralls",
                   "coveralls"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only"
    ],
    cmdclass = {'test': PyTest}
)
