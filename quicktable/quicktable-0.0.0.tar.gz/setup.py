from distutils.core import setup, Extension


quicktable = Extension(
    name='quicktable',
    sources=['lib/quicktable.c', 'lib/table.c']
)


setup(
    name='quicktable',
    version='0.0.0',
    author='Thomas Godkin',
    author_email='thgodkin+pypi@gmail.com',
    url='https://bitbucket.org/BooleanCat/quicktable/',
    ext_modules=[quicktable],
    include_dirs=['include']
)
