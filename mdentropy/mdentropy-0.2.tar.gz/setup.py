"""MDEntropy: Analyze correlated motions in MD trajectories with only a few
 lines of Python code.

MDEntropy is a python library that allows users to perform
 information-theoretic analyses on molecular dynamics (MD) trajectories.
"""
import sys
from setuptools import setup, find_packages

NAME = "mdentropy"
VERSION = "0.2"


def read(filename):
    import os
    BASE_DIR = os.path.dirname(__file__)
    filename = os.path.join(BASE_DIR, filename)
    with open(filename, 'r') as fi:
        return fi.read()


def readlist(filename):
    rows = read(filename).split("\n")
    rows = [x.strip() for x in rows if x.strip()]
    return list(rows)


extra = {}
if sys.version_info >= (3, 0):
    extra.update(
        use_2to3=True,
    )

setup(
    name=NAME,
    version=VERSION,
    scripts=['./scripts/dmutinf', './scripts/dtent'],
    platforms=["Windows", "Linux", "Mac OS-X", "Unix"],
    classifiers = (
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis',
        ),
    author="Carlos Xavier Hernandez",
    author_email="cxh@stanford.edu",
    url = 'https://github.com/cxhernandez/%s' % NAME,
    download_url = 'https://github.com/cxhernandez/%s/tarball/master' % NAME,
    description=("Analyze correlated motions in MD trajectories with only "
                 "a few lines of Python code."),
    license="MIT",
    packages = find_packages('mdentropy'),
    package_dir = {'': 'mdentropy'},
    include_package_data = True,
    package_data = {
        '': ['README.md',
             'requirements.txt'],
    },
    keywords="molecular dynamics entropy analysis",
    zip_safe=True,
    install_requires=readlist('requirements.txt'),
    **extra
)
