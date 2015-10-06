import os

from setuptools import setup


def read(f):
    here = os.path.abspath(os.path.dirname(__file__))
    return open(os.path.join(here, f), encoding='utf-8').read().strip()


setup(
    name='djed.static',
    version='0.5',
    description='Integration of BowerStatic into Pyramid for managing '
                'static resources with Bower',
    long_description='\n\n'.join((read('README.rst'), read('CHANGES.txt'))),
    classifiers=[
        "Framework :: Pyramid",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Internet :: WWW/HTTP",
    ],
    author='Djed developers',
    author_email='djedproject@googlegroups.com',
    url='https://github.com/djedproject/djed.static',
    license='ISC License (ISCL)',
    keywords='djed pyramid pylons bower static bowerstatic',
    packages=['djed.static'],
    include_package_data=True,
    install_requires=[
        'bowerstatic',
        'pyramid',
        'zope.interface',
    ],
    extras_require={
        'testing': [
            'djed.testing',
            'pyramid_chameleon',
        ],
    },
    test_suite='nose.collector',
)
