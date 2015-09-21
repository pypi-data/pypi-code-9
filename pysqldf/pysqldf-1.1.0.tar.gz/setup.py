from distutils.core import setup
from setuptools import find_packages


setup(
    name="pysqldf",
    version="1.1.0",
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
        "numpy",
        "pandas"
    ],
    tests_require=[
        "pandas",
        "nose"
    ]
)

