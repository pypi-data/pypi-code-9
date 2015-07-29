# python setup.py sdist upload
from setuptools import setup, find_packages

setup(
    name="gulag",
    description="Encapsulation convenience for mongo collections",
    version="0.43",
    author = "@jorjun",
    author_email="jorjuntech@icloud.com",
    url="https://bitbucket.org/jorjun/project_gulag",
    packages=['gulag'],
    install_requires=[
        "pymongo",
        "httplib2",
    ],
    keywords=["mongo", "mongodb", "pymongo"],
    license="Apache License, Version 2.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        'Programming Language :: Python',
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Database"],
)

