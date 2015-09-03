"""
Simple-Rss
"""

from setuptools import setup, find_packages

import simple_rss

PACKAGE = simple_rss

setup(
    name=PACKAGE.__NAME__,
    version=PACKAGE.__version__,
    license="MIT",
    author="Mardix",
    author_email='mardix@github.com',
    description="A simple simple RSS feed parser",
    long_description=PACKAGE.__doc__,
    url='http://github.com/mardix/simple-rss/',
    download_url='http://github.com/mardix/simple-rss/tarball/master',
    py_modules=['simple_rss'],
    include_package_data=True,
    install_requires=[
        "requests"
    ],

    keywords=["rss", "feed"],
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=find_packages(exclude=["test_config.py"]),
    zip_safe=False
)
