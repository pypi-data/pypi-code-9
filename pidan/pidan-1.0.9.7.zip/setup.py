# install:python setup.py sdist upload

from distutils.core import setup
 
setup (
    name = 'pidan',
    version = '1.0.9.7',
    packages=["pidan"],
    platforms=['any'],
    author = 'chengang',
    author_email = 'chengang.net@gmail.com',
    description = 'modify html.filter_tags2 function',
    package_data = {
        '': ['*.data'],
    },
)