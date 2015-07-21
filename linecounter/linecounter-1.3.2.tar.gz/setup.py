from distutils.core import setup

setup(name='linecounter',
      version='1.3.2',
      description='linecounter for files',
      long_description="""
Linecounter
===========

linecounter is a tool written in python, you can count how many lines you have in your files. This tool may be useful for developers who want to count how many lines of code they have in their projects. Because of linecounter isn't restricted for just code files it can be used in many areas which needs line counting.


Features
========

* Line counting for given file/files
* Line counting for list of files in given directory
* Line counting for list of files in given directory recursively
* Line counting for list of files in given directory with filtering file extensions
* Line counting without empty lines


Source
======

Find the latest version on github: https://github.com/halitkarakis/line-counter

Feel free to fork and contribute!

Installation
============

The easiest way to install is with pip::

    pip install linecounter

Or manually::

    python setup.py install


Usage
=====

Usage::

    linecounter -fd [-r] path1 [path2 ...] [--filter ext1 [ext2 ...]]

options::

    -f         Run line-counter with file paths
    -d         Run line-counter with directory paths
    -r         Search directories recursively, can be used if '-d' is set
    --filter   Count lines for files which extension is ext1, ext2 ...,
               can be used if '-d' is set
    --help     Show this message
    --version  Show version info
    --noempty  Count non-empty lines


Author
======

I'm Muhammet Halit Karakis from Istanbul, Turkiye. You can contact me by email halit (at) halitkarakis com tr
""",
      url='https://github.com/halitkarakis/line-counter/',
      py_modules=['linecounter'],
      author='M.Halit Karakis',
      author_email='halit@halitkarakis.com.tr',
      entry_points={
        'console_scripts': [
            'linecounter=linecounter:main',
        ],
      },
      license='Apache Software License',
      keywords='line counting tool command line',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Information Technology',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: Unix',
          'Programming Language :: Python',
          'Topic :: Text Processing',
          'Topic :: Text Processing :: General',
          'Topic :: Utilities',
          ],
      )