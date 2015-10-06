import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
	README = readme.read()
	
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="mezzanine-sue",
    version="0.2.6",
    packages=['sue'],
    include_package_data=True,
    license="BSD License",
    description="A theme for Mezzanine",
    long_description=README,
    url="https://github.com/lillisgary/mezzanine-newsue.git",
    author="Gary Lillis",
    author_email="lillisgary@gmail.com",
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
    ],
)
        
