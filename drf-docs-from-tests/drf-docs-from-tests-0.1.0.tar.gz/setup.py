# -*- coding: utf-8 -*-

from setuptools import setup

DESCRIPTION = """
More: https://github.com/scailer/drf-docs-from-tests
"""

setup(
    name='drf-docs-from-tests',
    version='0.1.0',
    author='Dmitriy Vlasov',
    author_email='scailer@yandex.ru',

    include_package_data=True,
    packages=['docsfromtests'],
    package_data={
        'docsfromtests': ['templates/*.html'],
    },

    url='https://github.com/scailer/drf-docs-from-tests/',
    license='MIT license',
    description='Stuff for generating docs from api-tests (djangorestframework).',
    long_description=DESCRIPTION,

    install_requires=[
        'djangorestframework'
    ],

    classifiers=(
        'Framework :: Django',
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ),
)
