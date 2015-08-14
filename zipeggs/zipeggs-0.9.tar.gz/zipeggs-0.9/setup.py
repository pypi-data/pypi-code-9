import os
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(
    name = "zipeggs",
    version="0.9",
    description="Zip back the eggs which are flattened by buildout",
    long_description=README,
    classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
    ],
    author='Azhagu Selvan SP',
    author_email='tamizhgeek@gmail.com',
    url='https://github.com/tamizhgeek/zipeggs',
    keywords="buildout zip recipe python",
    include_package_data=True,
    entry_points = {'zc.buildout': ['zipeggs = zipeggs:ZipEggs']},
    )
