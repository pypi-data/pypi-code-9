from distutils.core import setup
 
setup (
    name = 'pidan',
    version = '1.0.3',
    packages=["pidan"],
    platforms=['any'],
    author = 'chengang',
    author_email = 'chengang.net@gmail.com',
    description = 'http,html and convert modules',
    package_data = {
        '': ['*.data'],
    },
)