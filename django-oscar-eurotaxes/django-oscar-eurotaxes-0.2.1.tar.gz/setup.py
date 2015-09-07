# coding=utf-8
__copyright__ = 'Copyright 2015, Abalt'

from setuptools import setup, find_packages

VERSION = __import__('eurotaxes').get_version()


setup(
    name='django-oscar-eurotaxes',
    version=VERSION,
    url='https://bitbucket.org/abalt/django-oscar-eurotaxes',
    author='Abalt',
    author_email='admin@abalt.org',
    description=(
        "Package to manage taxes with django-oscar if the company must accomplish the European Laws of Taxes"),
    long_description=open('README.rst').read(),
    keywords="Taxes, Oscar",
    license=open('LICENSE').read(),
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    extras_require={
        'oscar': ["django-oscar>=0.6"]
    },
    download_url='https://bitbucket.org/abalt/django-oscar-eurotaxes/get/0.2.1.zip',
    # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Other/Nonlisted Topic'],
)
