from distutils.core import setup, Extension

pkcs11_version = "1.0.4"

ext = Extension("pkcs11",
                ["StdAfx.cpp", "pkcs11.cpp", "pkcs11_session.cpp", "pkcs11_structs.cpp", "pkcs11.rc", 'constants.cpp', "StdAfx.h", "pkcs11.h"],
                include_dirs = [".\\cryptoki"],
                define_macros = [('PKCS11_EXPORTS', None), ('PKCS11_VERSION', '\\"%s\\"' % pkcs11_version)],
                libraries = [])

setup(name = "pkcs11",
      version = pkcs11_version,
      description = "Python object-oriented wrapper for PKCS11 (Cryptoki) dlls",
      long_description = """The C++ extension module provides a nice object-oriented wrapper around a
binary PKCS11 module such as the PSM which comes as part of mozilla or the
various modules supplied by vendors of hardware crypto tokens.
        
The interface is somewhat limited as I only covered enough of it to handle the
functions defined in the module I care most about (for the Dallas
Semiconductor Java iButton) which for actual crypto operations only defines
signing hashes and unwrapping keys (browser handles the rest).""",
      author = "Jens B. Jorgensen",
      author_email = "jbj1@ultraemail.net",
      maintainer = "Jens B. Jorgensen",
      maintainer_email = "jbj1@ultraemail.net",
      license = "GPL",
      platforms = ["Win32",],
      keywords = ['crypto', 'pki', 'pkcs11', 'c++'],
      url = "http://www.ultraemail.net:8000/~jbj1/#pkcs11",
      download_url = "http://www.ultraemail.net:8000/~jbj1/pkcs11-%s.zip" % pkcs11_version,
      classifiers = ['Development Status :: 5 - Production/Stable',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: GNU General Public License (GPL)',
                     'Natural Language :: English',
                     'Operating System :: Microsoft :: Windows',
                     'Programming Language :: C++',
                     'Topic :: Security :: Cryptography',
                     'Topic :: Software Development :: Libraries :: Python Modules',
                     ],
      ext_modules = [ext],
      scripts = ["pkcs11test.py",])
