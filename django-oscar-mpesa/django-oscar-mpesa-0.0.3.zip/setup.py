#!/usr/bin/env python
from setuptools import setup, find_packages

from mpesa import get_version

setup(
    name='django-oscar-mpesa',
    version=get_version(),
    url='https://bitbucket.org/regulusweb/django-oscar-mpesa',
    author="Regulus Ltd",
    author_email="reg@regulusweb.com",
    description=("Oscar integration for M-Pesa's IPN service."),
    long_description=open('README.rst').read(),
    keywords="Payment, M-Pesa, IPN, Pay Bill, Oscar",
    license="BSD",
    platforms=['linux'],
    packages=find_packages(exclude=['sandbox*', 'tests*']),
    include_package_data=True,
    install_requires=[
        'django<1.9',
        'django-phonenumber-field==0.6.0',
        'django-oscar>=1.0.0',
        'jsonfield==1.0.3',
    ],
    extras_require={
    },
    # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Other/Nonlisted Topic'],
)
