from distutils.core import setup

setup(
    name='litelog',
    version='0.1.0',
    author='Matthew Cotton',
    author_email='matt@thecottons.com',
    packages=[
        'litelog',
    ],
    # scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    url='http://pypi.python.org/pypi/litelog/',
    license='LICENSE.txt',
    description='Simplified, robust, selective, recursive logging utility for Python.',
    long_description=open('README.txt').read(),
    install_requires=[],
)
