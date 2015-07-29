from distutils.core import setup

setup(
    name="mysql-replay",
    version="0.1.0",
    author="Hugo Chinchilla",
    author_email="hchinchilla@habitissimo.com",
    packages=["mysql"],
    include_package_data=True,
    description="Replay queries from a mysql slow log",
    install_requires=[
        "argparse",
        "mysqlclient",
    ],
)
