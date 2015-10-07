# -*- coding: UTF-8 -*-

from distutils.core import setup

# http://stackoverflow.com/a/7071358/735926
import re
VERSIONFILE='omitempty/__init__.py'
verstrline = open(VERSIONFILE, 'rt').read()
VSRE = r'^__version__\s+=\s+[\'"]([^\'"]+)[\'"]'
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % VERSIONFILE)

setup(
    name='omitempty',
    version=verstr,
    author='Baptiste Fontaine',
    author_email='b@ptistefontaine.fr',
    packages=['omitempty'],
    url='https://github.com/bfontaine/omitempty',
    license=open('LICENSE', 'r').read(),
    description='enums for Python',
    long_description="""\
omitempty is a Golang's omitempty equivalent for Python""",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
)
