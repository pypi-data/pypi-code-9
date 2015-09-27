from setuptools import find_packages, setup
from os.path import dirname, join

setup(
    name = 'helloworld-2015',
    version = '1.0.0',
    description = 'just for fun!',
    author = 'Anton Romanov',
    author_email = 'romanov.antoha@gmail.com',
    license = "BSD",
    url = 'https://github.com/fervid',
    package_dir = {'': 'src'},
    packages = find_packages('src'),
    long_description = open(join(dirname(__file__), 'README.txt')).read(),
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License"
    ]
)
