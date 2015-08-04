import os
from setuptools import setup, find_packages


def listify(filename):
    return filter(None, open(filename, 'r').readlines())


def read_file(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    return open(filepath, 'r').read()

setup(
    name="python-smpp",
    version="0.1.6",
    url='http://github.com/praekelt/python-smpp',
    license='BSD',
    description="Python SMPP Library",
    long_description=read_file('README.rst'),
    author='Praekelt Foundation',
    author_email='dev@praekeltfoundation.org',
    packages=find_packages(),
    install_requires=['setuptools'].extend(listify('requirements.pip')),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
