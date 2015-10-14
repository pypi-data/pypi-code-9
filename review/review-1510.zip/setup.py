#!/usr/bin/env python
"""
This setup.py packages `upload.py` script from rietveld project
as `review.py` for PyPI, so that it could be called as::

  python -m review

To update PyPI package, issue::
   python refresh.py
   python setup.py sdist upload
"""

from distutils.core import setup

setup(
    name='review',
    version='1510',
    author='Google Inc. & Co.',
    author_email='codereview-discuss@googlegroups.com',
    url='http://codereview.appspot.com/',

    description='upload script for Rietveld code review tool',
    long_description="""
Usage::

    python -m review [options]

Changes:

 1510:a0a624f - 2015-10-14

 - Rietveld moved to GitHub, syncing to a0a624f

* Rietveld Home Page:   http://codereview.appspot.com/
* Rietveld Development: http://code.google.com/p/rietveld/
* This script: http://bitbucket.org/techtonik/python-review/
* Discussions: http://groups.google.com/group/codereview-discuss/
""",
    license='Apache 2.0',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],

    py_modules=['review'],
)
