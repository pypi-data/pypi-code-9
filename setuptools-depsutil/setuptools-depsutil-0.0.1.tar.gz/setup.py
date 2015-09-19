#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages

from setuptools_depsutil import deps_download


def main():
    description = 'setuptools command for dependency packages'

    setup(
        name='setuptools-depsutil',
        version='0.0.1',
        description=description,
        long_description=description,
        classifiers=[
            "Framework :: Setuptools Plugin",
            "Development Status :: 4 - Beta",
            "Programming Language :: Python",
            "Intended Audience :: Developers",
            "Operating System :: POSIX",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
        ],
        keywords='setuptools command',
        author='momijiame',
        url='https://github.com/momijiame/setuptools-depsutil',
        zip_safe=False,
        include_package_data=True,
        packages=find_packages(),
        install_requires=[],
        tests_require=[],
        setup_requires=[],
        cmdclass={
            'deps_download': deps_download.deps_download,
        },
        entry_points={
            'distutils.commands': [
                'deps_download = setuptools_depsutil.deps_download:deps_download',  # noqa
            ],
        }
    )


if __name__ == '__main__':
    main()
