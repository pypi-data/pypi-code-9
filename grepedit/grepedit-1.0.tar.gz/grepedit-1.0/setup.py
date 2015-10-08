from distutils.core import setup


setup(name="grepedit",
      version="1.0",
      description="edit the result of a grep and modify the original files",
      author="Drew Perttula",
      author_email="drewp@bigasterisk.com",
      url="http://bigasterisk.com/grepedit",
      download_url="http://projects.bigasterisk.com/grepedit-1.0.tar.gz",
      
      scripts=["grepedit"],

      classifiers=[ # http://www.python.org/pypi?:action=list_classifiers
    "Development Status :: 5 - Production/Stable",
    "Programming Language :: Python",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "Intended Audience :: System Administrators",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "Topic :: Text Editors :: Text Processing",
    ],
     )
