#! /usr/bin/env python
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='audman',
    version='0.3.2',
    description='Control the audacious media player.',
    long_description=long_description,
    # Author details
    author='Ed F. McCurdy',
    author_email='efmccurdy@rogers.com',
    url='https://pypi.python.org/pypi/audman',
    # Choose your license
    license='GPL3',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Environment :: Web Environment',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Desktop Environment',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Multimedia :: Sound/Audio :: Players',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    # What does your project relate to?
    keywords='media player remote control',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['Mako','wsgiref'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={},
    packages=['audman'],
    package_dir={'audman': 'audman'},
    include_package_data=True,
    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={'audman': ['*.png'
                             'favicon.ico'],
    },
    data_files=[('audman', ['audman/ic_play_arrow_black_48dp.png',
                            'audman/ic_stop_black_48dp.png',
                            'audman/ic_repeat_black_48dp.png',
                            'audman/ic_arrow_drop_down_black_24dp.png',
                            'audman/ic_arrow_drop_up_black_24dp.png',
                            'audman/ic_unfold_less_black_24dp.png',
                            'audman/ic_unfold_more_black_24dp.png',
                            'audman/ic_vertical_align_center_black_24dp.png',
                            'audman/ic_volume_down_black_48dp.png',
                            'audman/ic_volume_up_black_48dp.png',
                            'audman/ic_skip_next_black_48dp.png',
                            'audman/ic_skip_previous_black_48dp.png',
                            'audman/ic_pause_black_48dp.png',
                            'audman/ic_shuffle_black_48dp.png',
                            'audman/favicon.ico'])],
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.s
    scripts = [
        'runaudman'
    ]
)
