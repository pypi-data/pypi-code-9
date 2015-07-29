from setuptools import setup

setup(
    name="mysql_replay",
    version="0.1.20",
    author="Hugo Chinchilla",
    author_email="hchinchilla@habitissimo.com",
    url='https://pypi.python.org/pypi/mysql-replay',
    license='GPLv3',
    keywords='mysql bechmarking log slow',
    packages=[
        "mysql_replay",
        "mysql_replay.mysql",
        "mysql_replay.mysql.utilities",
        "mysql_replay.mysql.utilities.common",
    ],
    include_package_data=True,
    description="Replay queries from a mysql slow log",
    install_requires=[
        "mysqlclient",
    ],
    entry_points={
        'console_scripts': [
            'mysql-replay = mysql_replay.execute:main',
            'mysql-replay-prepare = mysql_replay.prepare:main',
        ],
    }
)
