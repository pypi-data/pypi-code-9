#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
import re
from setuptools import setup

with open("pysqldf/__init__.py", "rb") as f:
    version = str(ast.literal_eval(re.search(
        r"__version__\s+=\s+(.*)",
        f.read().decode("utf-8")).group(1)
    ))

setup(
    name="pysqldf",
    version=version,
    author="Ryoji Ishii",
    author_email="airtoxin@icloud.com",
    url="https://github.com/airtoxin/pysqldf",
    license="MIT",
    packages=["pysqldf"],
    package_dir={"pysqldf": "pysqldf"},
    package_data={"pysqldf": ["data/*.csv"]},
    description="sqldf for pandas",
    long_description=open("README.rst").read(),
    install_requires=[
        "pandas"
    ],
    tests_require=[
        "nose"
    ],
    keywords="sqldf pandas dataframe sql pandasql",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: SQL",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ]
)
