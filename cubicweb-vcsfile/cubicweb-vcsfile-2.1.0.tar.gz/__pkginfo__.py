# pylint: disable-msg=W0622
"""cubicweb-vcsfile packaging information"""

modname = 'vcsfile'
distname = "cubicweb-%s" % modname

numversion = (2, 1, 0)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = "Logilab"
author_email = "contact@logilab.fr"
web = 'http://www.cubicweb.org/project/%s' % distname
description = "component to integrate version control systems data into the CubicWeb framework"
classifiers = [
           'Environment :: Web Environment',
           'Framework :: CubicWeb',
           'Programming Language :: Python',
           'Programming Language :: JavaScript',
           ]

__depends__ = {'cubicweb': '>= 3.19',
               'cubicweb-localperms': '>= 0.1.0',
               'logilab-mtconverter': '>= 0.7.0',
               'logilab-common': '>= 0.59.0',
               'python-hglib': '>= 1.4',
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
data_files.append([join('share', 'doc', distname), [join('scripts', 'hgnotifhook.py')]])
# Note: here, you'll need to add subdirectories if you want
# them to be included in the debian package

scripts=('scripts/vcsfile-notifbroker',)
