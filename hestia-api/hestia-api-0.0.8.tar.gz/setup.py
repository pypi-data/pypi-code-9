import os.path
from setuptools import setup


# Utility function to read the contents of short files.
def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


install_requires = [
    l for l in read('requirements.txt').split('\n')
    if l and not l.startswith('#')]

setup(
    name='hestia-api',
    version=open("hestia/_version.py").readlines()[-1].split()[-1].strip("\"'"),
    description='Python library for accessing the hestia.io API',
    author_email='info@hestia.io',
    author='hestia.io',
    url='https://www.hestia.io',

    download_url='https://github.com/hestiaio/hestia-python-api/tarball/0.0.1',

    packages=['hestia'],

    install_requires=install_requires,
)