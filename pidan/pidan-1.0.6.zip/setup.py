from distutils.core import setup
 
setup (
    name = 'pidan',
    version = '1.0.6',
    packages=["pidan"],
    platforms=['any'],
    author = 'chengang',
    author_email = 'chengang.net@gmail.com',
    description = 'date module add get_date function',
    package_data = {
        '': ['*.data'],
    },
)