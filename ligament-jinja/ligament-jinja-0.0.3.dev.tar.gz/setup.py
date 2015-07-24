'''A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
'''

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ligament-jinja',
    version='0.0.3.dev',
    description='A jinja build task for ligament',
    url='http://github.com/Adjective-Object/ligament_jinja',
    author='Adjective-Object',
    author_email='mhuan13@gmail.com',
    license='Apache 2',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7'],

    keywords='ligament grunt build automation jinja',
    install_requires=['ligament>=0.0.3.dev', 'Jinja2>=2.7.3'],

    packages=["ligament_jinja"]
)
