# encoding=utf8
# The setup file

import sys
import os.path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

import mime

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

requirements = [ x.strip() for x in open('requirements.txt').readlines() ]

setup(
    name = 'pymime',
    version = mime.__version__,
    author = 'lipixun',
    author_email = 'lipixun@outlook.com',
    url = 'https://github.com/lipixun/pymime',
    packages = [ 'mime', 'mime.spec', 'mime.tools' ],
    package_dir = { '': 'src' },
    install_requires = requirements,
    license = 'LICENSE',
    description = 'Mime types spec and tools',
    long_description = open('README.md').read(),
    keywords = [ 'python', 'mimetypes', 'mime' ],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ]
)

