# pylint: disable-msg=W0622
"""cubicweb-i18ncontent application packaging information

Copyright (c) 2008-2011 LOGILAB S.A. (Paris, FRANCE).
http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""

distname = 'cubicweb-i18ncontent'
modname = distname.split('-', 1)[1]

numversion = (0, 2, 0)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
description = 'internationalized content system for the CubicWeb framework'
author = 'Logilab'
author_email = 'contact@logilab.fr'
web = 'http://www.cubicweb.org/project/%s' % distname
classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
    ]

__depends__ = {'cubicweb': '>= 3.19.0',
               }


# packaging ###

from os import listdir as _listdir
from os.path import join, isdir
from glob import glob

THIS_CUBE_DIR = join('share', 'cubicweb', 'cubes', modname)

def listdir(dirpath):
    return [join(dirpath, fname) for fname in _listdir(dirpath)
            if fname[0] != '.' and not fname.endswith('.pyc')
            and not fname.endswith('~')
            and not isdir(join(dirpath, fname))]

data_files = [
    # common files
    [THIS_CUBE_DIR, [fname for fname in glob('*.py') if fname != 'setup.py']],
    ]
# check for possible extended cube layout
for dirname in ('entities', 'views', 'sobjects', 'hooks', 'schema', 'data', 'i18n', 'migration', 'wdoc'):
    if isdir(dirname):
        data_files.append([join(THIS_CUBE_DIR, dirname), listdir(dirname)])
# Note: here, you'll need to add subdirectories if you want
# them to be included in the debian package
