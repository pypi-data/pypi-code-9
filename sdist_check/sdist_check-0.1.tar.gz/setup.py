import os
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

tests_path = os.path.join(os.path.dirname(__file__), 'tests')


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test"), ]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)                                # pragma: no cover


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

install_requires = [
    'setuptools',
    ]

tests_require = [
    'pytest >= 2.0.3',
    'pytest-xdist',
    'pytest-cov',
    'docutils',
    ]

docs_require = [
    'Sphinx',
    ]

setup(
    name="sdist_check",
    version="0.1",
    author="Uli Fouquet",
    author_email="uli@gnufix.de",
    description=(
        "setuptools sdist checker."),
    license="MIT",
    keywords="setuptools sdist check",
    url="https://github.com/ulif/sdist_check/",
    py_modules=["sdist_check", ],
    packages=[],
    namespace_packages=[],
    long_description=read('README.rst') + '\n\n\n' + read('CHANGES.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    include_package_data=False,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=dict(
        tests=tests_require,
        docs=docs_require,
        ),
    cmdclass={'test': PyTest},
    entry_points={
        "distutils.commands": [
            "sdist_check = sdist_check:sdist_check",
        ],
    },
)
