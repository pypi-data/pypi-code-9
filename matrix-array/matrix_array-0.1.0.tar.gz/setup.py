"""
PyMatrix is for easier multi-Dimension matrix manipulation iterface. 
It provide basic Matrix utilities and vector based operator for easy access and compute elements. 
PyMatrix will act as glue between pure mathmatical interface and fast numpy computation core. You deem vector as row or col vector. 
With this interface your life will be easier. This is originally designed in 2014 when I am not satisfied with numpy, pandas and so on.
Use them altogether, you will find more about the package. 
"""

import os
import sys

if sys.version_info[:2] < (3,4):
    raise Exception("Python version >= 3.4 required, we might consider support older version in the future")

CLASSIFIERS = """
Development Status :: 5 - Production/Stable
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: OSI Approved
Programming Language :: C
Programming Language :: Python
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
Programming Language :: Python :: Implementation :: CPython
Topic :: Software Development
Topic :: Scientific/Engineering
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Operating System :: Unix
Operating System :: MacOS
"""

#from distutils.core import setup
from setuptools import setup

meta = dict(name='matrix_array',
    version='%s.%s.%s'%(0,1,0),# Major, Minor, Maintenance
    description='N-Dimension Matrix Object Container for ubiquitous purposes',
    long_description=__doc__,
    download_url="https://github.com/yiakwy/PyMatrix3.git",
    license="MIT",
    classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f],
    platforms=["Windows", "Linux", "Solaris", "Mac OS-X", "Unix"],
    author='Wang Lei',
    author_email="lwang11@mtu.edu",
    url="www.yiak.co",
    packages=['matrix_array', 'utils'],
)

def setup_package():
    setup(**meta)

if __name__ == "__main__":
    setup_package()
