#!/usr/bin/env python

from distutils.core import setup

# patch distutils if it can't cope with the "classifiers" or
# "download_url" keywords
import sys
if sys.version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None

setup(name = 'threadpool',
    version = '1.2.2',
    description = 'Easy to use object-oriented thread pool framework',
    keywords = 'threads design pattern',
    author = 'Christopher Arndt',
    author_email = 'chris.arndt@web.de',
    url = 'http://chrisarndt.de/en/software/python/threadpool.html',
    download_url = 'http://chrisarndt.de/en/software/python/download/threadpool-1.2.2.tar.bz2',
    license = "Python license",
    long_description = """\
A thread pool is an object that maintains a pool of worker threads to perform
time consuming operations in parallel. It assigns jobs to the threads
by putting them in a work request queue, where they are picked up by the
next available thread. This then performs the requested operation in the
background and puts the results in a another queue.

The thread pool object can then collect the results from all threads from
this queue as soon as they become available or after all threads have
finished their work. It's also possible, to define callbacks to handle
each result as it comes in.
""",
    platforms = "POSIX, Windows, MacOS X",
    classifiers = [
      'Development Status :: 5 - Production/Stable',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: Python Software Foundation License',
      'Operating System :: Microsoft :: Windows',
      'Operating System :: POSIX',
      'Operating System :: MacOS :: MacOS X',
      'Programming Language :: Python',
      'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    py_modules  = ['threadpool']
)
