#!/usr/bin/env python

from setuptools import setup, os


setup(
    name='PyBabel-json-md',
    version='0.1.0',
    description='PyBabel json metadef (md) gettext strings extractor',
    author='Wayne Okuma',
    author_email='wayne.okuma@hpe.com',
    packages=['pybabel_json_md'],
    url="https://github.com/wkoathp/pybabel-json-md",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'babel',
    ],
    include_package_data=True,
    entry_points = """
        [babel.extractors]
        json_md = pybabel_json_md.extractor:extract_json_md
        """,
)
