from domingo import __version__
from setuptools import setup, find_packages


setup(
    author="hangarunderground",
    author_email="domingo@reelio.com",
    name="domingo",
    packages=find_packages(exclude=['domingo/tests/*']),
    version=__version__,
    url="https://github.com/hangarunderground/domingo",
    download_url=(
        "https://github.com/hangarunderground/domingo/tarball/" + __version__
    ),
    description="A django-like modelling interface for various schemaless dbs",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords=["django", "schema-less", "models", "data"],
    install_requires=[
        'django', 'pymongo==2.7.2', 'redis', 'mongomock==2.0.0', 'twisted'
    ],
    extras_require={'rethink': ['rethinkdb', ], }
)
