# coding: utf-8

import os
from setuptools import setup


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='dj-templated-mail',
    version='0.1',
    packages=['dj_templated_mail'],
    include_package_data=True,
    license='MIT License',
    description='Django app that provides possibility to render email messages from templates stored in DB.',
    url='https://github.com/oeegor/dj-templated-mail#django-templated-mail/',
    author='Egor Orlov',
    author_email='oeegor@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
