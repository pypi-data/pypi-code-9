"""
OncodriveFM
===========

OncodriveFM detects candidate cancer driver genes and pathways from catalogs of somatic mutations
in a cohort of tumors by computing the bias towards the accumulation of functional mutations (FM bias).
This novel approach avoids some known limitations of recurrence-based approaches,
such as the difficulty to estimate background mutation rate, and the fact that they usually fail to identify
lowly recurrently mutated driver genes.
"""

from setuptools import setup, find_packages

from oncodrivefm import VERSION, AUTHORS, CONTACT_EMAIL

setup(
    name="oncodrivefm",
    version=VERSION,
    packages=find_packages(),

    install_requires=[
        'numpy >= 1.9.0',
        'scipy >= 0.14.0',
        'pandas >= 0.14.1',
        'matplotlib >= 1.4.0',
        'statsmodels >= 0.5.0'
    ],

    entry_points={
        'console_scripts': [
            'oncodrivefm = oncodrivefm.command.full:main',
            'oncodrivefm-compute = oncodrivefm.command.compute:main',
            'oncodrivefm-combine = oncodrivefm.command.combine:main'
        ]
    },

    # metadata for upload to PyPI
    author=AUTHORS,
    author_email=CONTACT_EMAIL,
    description="OncodriveFM",
    license="UPF Free Source Code",
    keywords="",
    url="https://bitbucket.org/bbglab/oncodrivefm",
    download_url="https://bitbucket.org/bbglab/oncodrivefm/get/{}.tar.gz".format(VERSION),
    long_description=__doc__,

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ]
)
