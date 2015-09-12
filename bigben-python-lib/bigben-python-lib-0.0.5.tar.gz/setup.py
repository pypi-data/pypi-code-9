
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))



setup(
    name='bigben-python-lib',
    version='0.0.5',
    description='Client library used for interacting with BigBen APIs.',
    long_description='Client library used for interacting with BigBen APIs.',
    url='https://github.com/sgiroux/bigben-python-lib',
    author='Sam Giroux',
    author_email='giroux@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='BigBen',
    packages=find_packages(exclude=[]),
    install_requires=[],
)



