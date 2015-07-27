import os
from setuptools import setup

setup(
    name = "SimpleS3Backup",
    version = "0.1",
    author = "Dewey Sasser",
    author_email = "dewey@sasser.com",
    description = ("A simple backup script that saves artbitrary command output to s3 in a rotating series of files"),
    license = "Artistic License",
    keywords ="Amazon AWS S3 Backup",
    url = "https://github.com/deweysasser/SimpleS3Backup",
    scripts = ['s3backup'],
    long_description = '''Simple backup script to run commands and send the output to S3

    ./s3backup -bucket example-bucket -path backups -name mybackup.tar -count 3 tar -C /some/path cp .

Creates /backups/mybackup.tar.1 in AWS bucket "example-bucket", using
the default boto profile.  As you run it each day it will rotate up to
COUNT versions, then overwrite.

It uses local disk to store the file, then uploads to S3.''',
    install_requires=[ 'boto' ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: Artistic License"
        ],
)
