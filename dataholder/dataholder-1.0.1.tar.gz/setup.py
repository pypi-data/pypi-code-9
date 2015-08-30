#! ../env/bin/python
import os
import sys
import dataholder

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='dataholder',
    version=dataholder.__version__,
    description='Trick for assignment in an if statement',
    long_description=open('README.rst').read(),
    url='https://github.com/pitcons/dataholder',
    install_requires=[''],
    packages=['dataholder'],
    include_package_data=True,
    scripts=[],
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
    ),
    keywords='python',
)
