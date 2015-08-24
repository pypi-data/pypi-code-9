import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "fickr",
    version = "0.0.1",
    author = "Mathias Perlet",
    author_email = "mathias@mperlet.de",
    description = ("Download all flickr photos from a user"),
    license = "MIT",
    keywords = "flickr download dump",
    url = "http://github.com/mperlet/fickr.py",
    long_description=read('Readme.md'),
    scripts = ['fickr']
)
