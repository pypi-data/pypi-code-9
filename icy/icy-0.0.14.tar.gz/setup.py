from setuptools import setup
from icy import __version__

DESCRIPTION = 'data wrangling glue code'

LONG_DESCRIPTION = """
icy Python Package
------------------


Installation

* Activate Python 3.4 / 3.5 environment

* Run `pip install icy` or download and run `python setup.py install`


Usage

* `data = icy.read(path)` returns a dictionary of pandas.DataFrames.

* Path can be a folder or zip-, csv-, tsv-, txt-, json-, html-, (xml-,) xls-, xlsx-, sqlite-, hdf5-file and more.

* See the source at https://github.com/rcs-analytics/icy


Documentation

* Docs & Examples at https://www.rcs-analytics.com/icy/index.html


License

* MIT (https://github.com/rcs-analytics/icy/blob/master/LICENSE)


© 2015 Jonathan Rahn, RCS Analytics GmbH, https://www.rcs-analytics.com
"""

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3 :: Only',
    'Topic :: Scientific/Engineering',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

if __name__ == '__main__':
    setup(
        name = 'icy',
        version = __version__,
        description = DESCRIPTION,
        install_requires = ['pandas', 'pyyaml', 'odo'],
        author = 'Jonathan Rahn',
        author_email = 'jr@rcs-analytics.com',
        url = 'https://github.com/rcs-analytics/icy',
        download_url = '',
        license = 'MIT',
        packages = ['icy'],
        long_description = LONG_DESCRIPTION,
        platforms = 'any',
        classifiers = CLASSIFIERS,
    )
