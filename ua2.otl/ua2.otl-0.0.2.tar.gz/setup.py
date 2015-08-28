#!/usr/bin/env python
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


Name='ua2.otl'
ProjecUrl="https://bitbucket.org/ua2crm/ua2.otl"
Version='0.0.2'
Author='Vic Bukhantsov'
AuthorEmail='vic@ua2crm.com'
Maintainer='Viacheslav Vic Bukhantsov'
Summary='Django one time link generator and processor'
License='BSD License'
ShortDescription=Summary

with open('README.rst') as fh:
    long_description = fh.read()

needed = [
    'ua2.redis>=0.0.2',
    'Django>=1.4.0',
]

EagerResources = [
    'ua2',
]

ProjectScripts = [
##    'scripts/runweb',
]

PackageData = {
    '': ['*.*', '*.html'],
}

# Make exe versions of the scripts:
EntryPoints = {
}

setup(
    url=ProjecUrl,
    name=Name,
    zip_safe=False,
    version=Version,
    author=Author,
    author_email=AuthorEmail,
    description=ShortDescription,
    long_description=long_description,
    license=License,
    scripts=ProjectScripts,
    install_requires=needed,
    include_package_data=True,
    packages=find_packages('src'),
    package_data=PackageData,
    package_dir = {'': 'src'},
    eager_resources = EagerResources,
    entry_points = EntryPoints,
    namespace_packages = ['ua2'],
)
