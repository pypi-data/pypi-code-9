# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'docs/index.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ThinkTogether',
    version='1.0.0',

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
