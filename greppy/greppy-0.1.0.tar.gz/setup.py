import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="greppy",
    version="0.1.0",
    author="iLoveTux",
    author_email="me@ilovetux.com",
    description=("A grep replica (I'd say clone, but not quite)"),
    license="GPLv3",
    keywords="grep regex",
    url="http://github.com/ilovetux/greppy",
    packages=['greppy'],
    entry_points={
        "console_scripts": ["grep.py=greppy:_main"]
    },
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ]
)
