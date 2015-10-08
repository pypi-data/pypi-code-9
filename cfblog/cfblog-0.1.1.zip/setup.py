# -*- coding: utf-8 -*-
from setuptools import setup

try:
    long_description = open('README.rst', 'rt').read()
except Exception:
    long_description = ""

setup(
    name="cfblog",
    description="Awesome CMS for Django",
    long_description=long_description,

    version="0.1.1",
    author='Vinay Karanam',
    author_email="vinayinvicible@gmail.com",

    url='https://github.com/Coverfox/cfblog/',
    license='BSD',

    install_requires=[
        "fhurl>=0.1.7", "smarturls", "six", "Django>=1.3",
        "dj-database-url",
    ],
    packages=['cfblog', 'cfblog.migrations'],

    zip_safe=True,
)
