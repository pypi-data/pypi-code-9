#!/usr/bin/env python

from distutils.core import setup, Extension

module1 = Extension('skip32', sources = ['skip32.c'])

NAME         = "skip32"
DESCRIPTION  = 'implementation of skip32 based on http://search.cpan.org/~esh/Crypt-Skip32-0.08/lib/Crypt/Skip32.pm',
AUTHOR       = "Jefurry"
AUTHOR_EMAIL = "jefurry@qq.com"
URL          = "http://www.penqie.com"
VERSION      = "1.3"

setup (name              = NAME,
        version          = VERSION,
        keywords         = 'skip32',
        description      = DESCRIPTION,
        dependency_links = [],
        install_requires = [],
        url              = URL,
        license          = "LGPL",
        ext_modules      = [module1],
        author           = AUTHOR,
        author_email     = AUTHOR_EMAIL,
        scripts          = [])

