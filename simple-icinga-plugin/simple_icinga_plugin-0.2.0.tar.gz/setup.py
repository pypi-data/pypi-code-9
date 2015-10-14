"""
simple_icinga_plugin setup module.
"""

from setuptools import setup

setup(
    name='simple_icinga_plugin',
    version='0.2.0',
    description='simple icinga plugin helper module',
    url='https://github.com/vshn/simple_icinga_plugin',
    author='Andre Keller',
    author_email='andre.keller@vshn.ch',
    # BSD 3-Clause License:
    # - http://opensource.org/licenses/BSD-3-Clause
    license='BSD',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    packages=[
        'simple_icinga_plugin',
    ]

)
