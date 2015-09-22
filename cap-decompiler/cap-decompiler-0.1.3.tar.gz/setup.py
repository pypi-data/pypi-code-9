import os
from setuptools import setup, find_packages
from codecs import open
from os import path

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='cap-decompiler',
    version='0.1.3',
    packages=find_packages(),
    install_requires=['capstone'],
    include_package_data=True,
    license='BSD Licence',  
    description='Credits for starting project goes to the https://github.com/EiNSTeiN-',
    long_description=README,
    url='http://starp1rate.github.io/',
    author='starp1rate',
    author_email='spiperac@denkei.org',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
	'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',	
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
