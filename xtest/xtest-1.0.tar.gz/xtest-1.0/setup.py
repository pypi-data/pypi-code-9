from distutils.core import setup
from distutils.extension import Extension
from Pyrex.Distutils import build_ext

setup(name="xtest",
      version="1.0",
      description="pyrex interface to XTest including faking multi-key presses such as Control-Shift-s",
      author="Drew Perttula",
      author_email="drewp@bigasterisk.com",
      url="http://bigasterisk.com",
      download_url="http://projects.bigasterisk.com/",
      classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Operating System :: POSIX :: Linux',
    'Environment :: X11 Applications',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    ],
      
      ext_modules=[
        Extension("xtest",
                  ["xtest.pyx"],
                  library_dirs=['/usr/X11R6/lib'],
                  libraries=["X11","Xtst"]),
        ],  
      cmdclass={'build_ext':build_ext},
)

