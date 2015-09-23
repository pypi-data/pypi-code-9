# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path


long_description = \
"""
ThinkTogether
-----
ThinkTogether is a light-weight package that implements classes designed to reimagine modular learning, research, and development-oriented inquiry.  
ThinkTogether embodies and enforces an information hierarchy that segments analysis cleanly into two parts: gathering and processing.

ThinkingTogether Builds Complex Systems
````````````
ThinkTogether may be imagined as the building blocks of a large-scale research project. The bricks are InformationSets and InferenceSets, and the roof is the Collection, which ties a project together into an easily accessible object. All three classes extend Python’s native dictionary class.
.. code:: python
	from ThinkTogether import InformationSet, InferenceSet, Collection

Links
`````
* `documentation <https://pythonhosted.org/ThinkTogether>`_
* `development
  <http://github.com/iamjarret/ThinkTogether>`_
"""

setup(
    name='ThinkTogether',
    version='1.0.1',

    description='ThinkTogether: Imagining Inquiry-Based Collaboration',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/iamjarret/ThinkTogether',

    # Author details
    author='Jarret Petrillo',
    author_email='jarret@empirecapitalre.com',

    # Choose your license
    license='BSD',
    platforms='any',
    data_files = [('', ['LICENSE.txt'])],

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Operating System :: OS Independent',


        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: BSD License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
    ],

    # What does your project relate to?
    keywords='system design information architecture',
)
