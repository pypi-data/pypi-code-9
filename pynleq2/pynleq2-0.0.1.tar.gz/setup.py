#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
pynleq2 is a python binding for NLEQ2.

NLEQ2 is part of the CodeLib collection of algortihms:
http://elib.zib.de/pub/elib/codelib/en/

Retrieved on 2015-10-20 13:25:

   /.../
   The ZIB-CodeLib software may be used for scientific and educational purposes
   free of charge. For commercial use of the software you must sign a license-
   agreement with the ZIB and pay a license-charge that depends on the
   referenced software package and the intended usage. Please read our sample
   license agreement for more details.

http://elib.zib.de/pub/elib/codelib/en/Lizenz.html

In order to indicate that you have read and accepted their license
you need to either:

- set the environment variable PYNLEQ2_NLEQ2_ROOT_URL to
  point to a repository containing the source code of NLEQ2. e.g.
     $ export PYNLEQ2_NLEQ2_ROOT_URL=http://www.univeristy.edu/mirror/nleq2/

- Alternatively, extract the sources into the nleq2/ sub-directory manually.


The python interface (nleq2/nleq2.pyf) has been taken from the BSD licensed
PySCeS project (http://pysces.sourceforge.net/), see also LICENSE_pysces.txt

This has been tested vid NLEQ2 v 2.3.0.2
"""

import os
import shutil
import sys
from numpy.distutils.core import setup, Extension

pkg_name = 'pynleq2'

ext_modules = []
if len(sys.argv) > 1 and '--help' not in sys.argv[1:] and sys.argv[1] not in (
        '--help-commands', 'egg_info', 'clean', '--version'):
    # nleq2 version: 2.3.0.2
    md5output = """\
    28ed88f1ae7bab8dc850348b5e734881  linalg_nleq2.f
    73401c84c8e0d434fffa6f303ba813e0  nleq2.f
    77189300200be5748152fa28dc236963  wnorm.f
    5d912441fb6f55d10c8b98bbb9168195  zibconst.f
    e2ac1a20fc6294cb3e0d7f65bbac53e6  zibmon.f
    6520c958f2bd339b435a68541d5b910b  zibsec.f
    """
    from textwrap import dedent
    md5sums, sources = zip(*map(str.split, dedent(md5output)[:-1].split('\n')))

    def md5_of_file(path, nblocks=128):
        from hashlib import md5
        md = md5()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(nblocks*md.block_size), b''):
                md.update(chunk)
        return md

    def download(url, outpath):
        from urllib2 import urlopen
        f = urlopen(url)
        print("downloading " + url)
        with open(outpath, "wb") as fh:
            fh.write(f.read())

    for src, md5sum in zip(sources, md5sums):
        srcpath = os.path.join('nleq2', src)
        if not os.path.exists(srcpath):
            NLEQ2_URL = os.environ.get('PYNLEQ2_NLEQ2_ROOT_URL', None)
            if NLEQ2_URL:
                download(NLEQ2_URL+src, srcpath)
            else:
                fmtstr = "Could not find: %s ($PYNLEQ2_NLEQ2_ROOT_URL not set)"
                raise ValueError(fmtstr % src)
        if md5_of_file(srcpath).hexdigest() != md5sum:
            raise ValueError("Mismatching MD5 sum for %s" % srcpath)

    ext_modules = [
        Extension('pynleq2.nleq2', [os.path.join('nleq2', f)
                                    for f in ('nleq2.pyf',) + sources])
    ]

PYNLEQ2_RELEASE_VERSION = os.environ.get('PYNLEQ2_RELEASE_VERSION', '')

# http://conda.pydata.org/docs/build.html#environment-variables-set-during-the-build-process
CONDA_BUILD = os.environ.get('CONDA_BUILD', '0') == '1'
if CONDA_BUILD:
    try:
        PYNLEQ2_RELEASE_VERSION = 'v' + open(
            '__conda_version__.txt', 'rt').readline().rstrip()
    except IOError:
        pass

release_py_path = os.path.join(pkg_name, '_release.py')

if (len(PYNLEQ2_RELEASE_VERSION) > 1 and
   PYNLEQ2_RELEASE_VERSION[0] == 'v'):
    TAGGED_RELEASE = True
    __version__ = PYNLEQ2_RELEASE_VERSION[1:]
else:
    TAGGED_RELEASE = False
    # read __version__ attribute from _release.py:
    exec(open(release_py_path).read())

classifiers = [
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Fortran',
    'Programming Language :: Python',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Mathematics',
]

tests = [
    'pynleq2.tests',
]

descr = "Python binding for NLEQ2"
setup_kwargs = dict(
    name=pkg_name,
    version=__version__,
    description=descr,
    classifiers=classifiers,
    author='Björn Dahlgren',
    author_email='bjodah@DELETEMEgmail.com',
    url='https://github.com/bjodah/' + pkg_name,
    license='BSD',
    requires=['numpy'],
    packages=[pkg_name] + tests,
    ext_modules=ext_modules,
)

if __name__ == '__main__':
    try:
        if TAGGED_RELEASE:
            # Same commit should generate different sdist
            # depending on tagged version (set PYNLEQ2_RELEASE_VERSION)
            # this will ensure source distributions contain the correct version
            shutil.move(release_py_path, release_py_path+'__temp__')
            open(release_py_path, 'wt').write(
                "__version__ = '{}'\n".format(__version__))
        setup(**setup_kwargs)
    finally:
        if TAGGED_RELEASE:
            shutil.move(release_py_path+'__temp__', release_py_path)
