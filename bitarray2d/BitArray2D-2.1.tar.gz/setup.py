#!/usr/bin/env python

### setup.py

from distutils.core import setup

setup(name='BitArray2D',
      version='2.1',
      author='Avinash Kak',
      author_email='kak@purdue.edu',
      maintainer='Avinash Kak',
      maintainer_email='kak@purdue.edu',
      url='http://RVL4.ecn.purdue.edu/~kak/dist2d/BitArray2D-2.1.html',
      download_url='http://RVL4.ecn.purdue.edu/~kak/dist2d/BitArray2D-2.1.tar.gz?download',
      description='A memory-efficient packed representation for 2D bit arrays (This is a renamed version of the Bit2DArray module',
      long_description=''' 

**Version 2.1** is a renamed version of the Bit2DArray module (Version 2.0).

**Version 2.1** is Python 3.x compliant.  It should work with both Python
2.x and Python 3.x.

This module utilizes the facilities of the **BitVector** class (Version 3.0
or higher) to create a memory efficient representation for 2D bit arrays.

The class supports the following operators/methods:

-    __str__
-    __getitem__
-    __setitem__
-    __getslice__
-    __eq__
-    __ne__
-    __and__
-    __or__
-    __xor__
-    __invert__
-    deep_copy
-    size
-    read_bit_array_from_char_file
-    read_bit_array_from_binary_file
-    write_bit_array_to_char_file
-    write_bit_array_to_packed_binary_file
-    shift
-    dilate
-    erode

          ''',

      license='Python Software Foundation License',
      keywords='2D bit array, binary image, 2D bit field',
      platforms='All platforms',
      classifiers=['Topic :: Utilities', 'Programming Language :: Python'],
      packages=['']
)
