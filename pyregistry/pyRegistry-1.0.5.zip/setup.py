from distutils.core import setup, Extension

ext = Extension("pyRegistry",
                ["StdAfx.cpp", "pyRegistry.cpp", "pyRegistry.rc"],
                define_macros= [('PYREGISTRY_EXPORTS', None)],
                libraries = ["advapi32"])

setup(name = "pyRegistry",
      version = "1.0.5",
      author = "Jens B. Jorgensen",
      author_email = "jbj1@ultraemail.net",
      maintainer = "Jens B. Jorgensen",
      maintainer_email = "jbj1@ultraemail.net",
      url = "http://jbox.ultraemail.net:8000/~jbj1/",
      license = "GPL",
      description = "object-oriented interface to the Windows Registry",
      long_description = """Python 2.X extension module for windows that gives you object-oriented python-
style access to the Windows Registry. Highlights: 

 * can get HKEY_PERFORMANCE_DATA, handles REG_MULTI_SZ (==> 
['string', 'string']) 
 * handles python unicode strings 
 * has no dependencies on win32* modules.""",
      keywords = "windows registry",
      platforms = "win32",
      download_url = "http://jbox.ultraemail.net:8000/~jbj1/pyRegistry/pyRegistry-1.0.5.zip",
      classifiers = [
            'Development Status :: 5 - Production/Stable',
            'Environment :: Win32 (MS Windows)',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Natural Language :: English',
            'Operating System :: Microsoft :: Windows',
            'Programming Language :: C++',
            'Topic :: Software Development :: Libraries :: Python Modules'
            ],
      ext_modules = [ext])
