import os
from setuptools import setup

read = lambda f_name: open(os.path.join(os.path.dirname(__file__), f_name)).read()

PACKAGE_NAME = 'FlyForms'
PACKAGE_VERSION = '0.2.0'
AUTHOR = 'Pavel Sizov'
AUTHOR_EMAIL = 'shabash1991@yandex.ru'

setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    url='https://bitbucket.org/ShabashP/flyforms',
    license='MIT',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description='FlyForms is flexible and easy to use Python library for data structures defining and validation.',
    long_description=read("README.rst"),
    keywords='validation, structures, form, forms, validator, schema, data',
    packages=[
        'flyforms',
    ],
    test_suite='tests.runtests',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5'
    ]
)
