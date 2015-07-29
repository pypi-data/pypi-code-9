from setuptools import setup

setup(
    name="mysql-replay",
    version="0.1.6",
    author="Hugo Chinchilla",
    author_email="hchinchilla@habitissimo.com",
    url='https://pypi.python.org/pypi/mysql-replay',
    license='GPLv3',
    keywords='mysql bechmarking log slow',
    packages=["mysql.utilities", "mysql.utilities.common"],
    include_package_data=True,
    description="Replay queries from a mysql slow log",
    install_requires=[
        "mysqlclient",
    ],
    entry_points={
        'console_scripts': [
            'mysql-replay = execute:main',
            'mysql-replay-prepare = prepare:main',
        ],
    }
)
