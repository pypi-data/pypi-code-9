from distutils.core import setup, Extension

ext = Extension("PyCY",
                ["PyCY.cpp"],
                include_dirs = [],
                define_macros = [('PYREGISTRY_EXPORTS', None)],
                library_dirs = [],
                libraries = [])

setup(name = "PyCY",
      version = "1.0.0",
      description = "Windows CY type wrapper",
      author = "Jens B. Jorgensen",
      author_email = "jbj1@ultraemail.net",
      url = "http://www.ultraemail.net/~jbj1",
      ext_modules = [ext])
