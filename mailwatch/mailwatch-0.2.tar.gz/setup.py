#!/usr/bin/python -tt

import mw


from distutils.core import setup
setup(name='mailwatch',
      version=mw.__version__,
      description='Mailwatcher for Maildirs',
      author=mw.__author__,
      author_email=mw.__author_email__,
      url="http://www.schwarzvogel.de/software-misc.shtml",
      download_url="http://www.schwarzvogel.de/pkgs/mailwatch-%s.tar.gz" % 
        (mw.__version__),
      scripts = ["mw.py"],
      data_files = [("share/doc/mw-%s/" % (mw.__version__), 
        ['README', 'COPYING', 'mw.1'])],
      )

