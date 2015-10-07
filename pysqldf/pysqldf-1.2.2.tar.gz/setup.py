from distutils.core import setup
from setuptools import find_packages


setup(
    name="pysqldf",
    version="1.2.2",
    author="Ryoji Ishii",
    author_email="airtoxin@icloud.com",
    url="https://github.com/airtoxin/pysqldf/",
    license="MIT",
    packages=find_packages(),
    package_dir={"pysqldf": "pysqldf"},
    package_data={"pysqldf": ["data/*.csv"]},
    description="sqldf for pandas",
    long_description=open("README.rst").read(),
    install_requires=[
        "pandas"
    ],
    tests_require=[
        "pandas",
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

