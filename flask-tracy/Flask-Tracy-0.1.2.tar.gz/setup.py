#!/usr/bin/env python

from setuptools import setup, find_packages


with open('README.rst') as file:
    readme = file.read()


setup(
    name='Flask-Tracy',
    version='0.1.2',
    url='https://github.com/juztin/flask-tracy',
    license='BSD',
    author='Justin Wilson',
    author_email='justin@minty.io',
    description='Logs tracing information on a per-request basis',
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask>=0.9',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3 :: Only",
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
