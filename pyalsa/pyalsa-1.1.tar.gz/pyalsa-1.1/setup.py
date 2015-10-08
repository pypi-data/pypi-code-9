from distutils.core import setup
from distutils.extension import Extension
from Pyrex.Distutils import build_ext
setup(
  name = "pyalsa",
  version="1.1",
  description="limited bindings to alsa audio lib",
  
  long_description="""

  cvs is available:
    cvs -z3 -d :pserver:anonymous@bigasterisk.com:/srcmirror co pyalsa
  also viewcvs:
    http://cvs.bigasterisk.com/viewcvs/pyalsa/
  
  Module was written for use with my cuisine video editor system
  (cuisine.bigasterisk.com).

  Currently supports opening pcm for nonblocking output and writing
  interleaved samples. I may add mixer support, as I wish to control
  my volume and sblive routing.

  Api is subject to change, but it will probably stay inspired by the
  alsa api and alsa example code.""",
  
  author="Drew Perttula",
  author_email="drewp@bigasterisk.com",
  url="http://bigasterisk.com",
  download_url="http://bigasterisk.com/post/pyalsa-1.0.tar.gz",
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python',
    'Topic :: Multimedia :: Sound/Audio :: Players',
    'Topic :: Software Development :: Libraries :: Python Modules',
    ],
  ext_modules=[ 
    Extension("pyalsa", ["pyalsa.pyx"], libraries = ["asound"])
    ],
  cmdclass = {'build_ext': build_ext}
)
