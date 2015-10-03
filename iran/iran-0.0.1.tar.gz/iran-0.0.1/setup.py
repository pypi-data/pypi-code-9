import glob
import imp
import io
import os
from os import path
from setuptools import setup, find_packages, Extension
import sys

MYDIR = path.abspath(os.path.dirname(__file__))

#VERSION = imp.load_source('version', path.join('.', 'wiwi', 'version.py'))
VERSION = '0.0.1'

# NOTE
REQUIRES = []

cmdclass = {}
ext_modules = []

setup(
    name='iran',
    version=VERSION,
    description='Python for iran.',
    #long_description=io.open('README.rst', 'r', encoding='utf-8').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: Jython',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='wsgi web api framework rest http cloud',
    author='Farsheed Ashouri',
    author_email='rodmena@me.com',
    url='https://github.com/ourway/iran',
    license='Apache 2.0',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIRES,
    setup_requires=[],
    cmdclass=cmdclass,
    ext_modules=ext_modules,
    test_suite='nose.collector',
    entry_points={
        'console_scripts': [
            'wiwi = wiwi.cmd:main'
        ]
    }
)
