#!/usr/bin/env python2.7
import nosescript
import setuptools


setuptools.setup(
    name='nosescript',
    version=nosescript.__version__,
    description="A Nose plugin for JavaScript tests.",
    zip_safe=False,
    url="https://github.com/simpoir/nosescript",
    author="Simon Poirier",
    author_email="simpoir+nosescript@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Testing",
    ],

    packages=setuptools.find_packages(exclude=[
        "*.tests", "*.tests.*", "tests.*", "tests",
    ]),
    include_package_data=True,
    setup_requires=[
        'wheel',
    ],
    install_requires=[
        'nose',
        'python-spidermonkey',
    ],
    tests_require=[
        'nose-cov',
        'flexmock',
    ],
    entry_points={
        'nose.plugins.0.10': [
            'nosescriptunit = nosescript.unit:NoseScriptUnit'
        ]
    }
)
