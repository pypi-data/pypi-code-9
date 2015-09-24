#!/usr/bin/env python

V = "0.1"

from distutils.core import setup
setup(name='tb',
      author='Skip Montanaro',
      author_email='skip@pobox.com',
      url='http://www.smontanaro.net/python/',
      download_url=('http://www.smontanaro.net/python/tb-%s.tar.gz' % V),
      version=V,
      description="Alternate traceback formatting functions",
      long_description="""
The tb module defines two functions, compact_traceback and
verbose_traceback, either of which can be assigned to sys.excepthook and
used as alternate traceback display functions.

Version %s is the first release.""" % V,
      py_modules=['tb'],
      license='MIT License',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.5',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries :: Python Modules',
          ]
      )
