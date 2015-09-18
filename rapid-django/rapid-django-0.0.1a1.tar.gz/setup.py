__author__ = 'marcos.medeiros'

"""Rapid-Django installation script
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
import os
from os import path

def _recursive_find(root, p):
    full_p = path.join(root, p)
    for f in os.listdir(full_p):
        full_f = path.join(full_p, f)
        val_f = path.join(p, f)
        if path.isdir(full_f):
            for ff in _recursive_find(root, val_f):
                yield ff
        else:
             yield val_f


here = path.abspath(path.dirname(__file__))
rapid = path.join('src', 'rapid')
rapid_files = list(_recursive_find(os.path.join(here, rapid), ''))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rapid-django',

    version='0.0.1a1',

    description='Opionated tools for rapid development of enterprise CRUD portals',
    long_description=long_description,

    # The project's main homepage.
    url='https://marcosdumay.com/rapid-django',

    # Author details
    author='Marcos Dumay de Medeiros',
    author_email='marcos@marcosdumay.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django :: 1.8',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        #'Programming Language :: Python :: 3',
        #'Programming Language :: Python :: 3.2',
        #'Programming Language :: Python :: 3.3',
        #'Programming Language :: Python :: 3.4',
    ],

    # What does your project relate to?
    keywords='CRUD',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['rapid'],
    package_dir = {'': 'src'},

    zip_safe = False,

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['django>=1.8', 'django-datetime-widget>=0.9', 'django-migration-fixture>=0.5', 'six'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={},

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.

    #include_package_data=True,
    package_data={
        'rapid': rapid_files,
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        # 'console_scripts': [
        #     'sample=sample:main',
        # ],
    },
)
