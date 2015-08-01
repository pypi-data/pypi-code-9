from distutils.core import setup

setup(
    name='litelog',
    version='0.1.6',
    author='Matthew Cotton',
    author_email='matt@thecottons.com',
    py_modules=['litelog',],
    # scripts=[],
    url='http://pypi.python.org/pypi/litelog/',
    license='LICENSE.txt',
    description='Simplified, robust, selective, recursive logging utility for Python.',
    long_description=open('README.txt').read(),
    install_requires=[],
)
