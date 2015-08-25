import os
import sys

import tzpos

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'tzpos'
]

requires = ['pytz']

setup(
    name='tzpos',   
    version=tzpos.__version__,
    description='Time zone name calculation from lon and lat database.',
    long_description=open('README.txt').read(),
    author='Gamaliel Espinoza Macedo',
    author_email='gamaliel.espinoza@gmail.com',
    url='',
    packages=packages,
    package_dir={'tzpos': 'tzpos'},
    install_requires=requires,
    include_package_data=True,
    package_data={
        'tzpos': ['*.data'],
    },
    zip_safe=False,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ),
)