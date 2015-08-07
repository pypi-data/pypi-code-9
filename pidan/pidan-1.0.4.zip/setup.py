from distutils.core import setup
 
setup (
    name = 'pidan',
    version = '1.0.4',
    packages=["pidan"],
    platforms=['any'],
    author = 'chengang',
    author_email = 'chengang.net@gmail.com',
    description = 'http module add strip_params_from_url function',
    package_data = {
        '': ['*.data'],
    },
)