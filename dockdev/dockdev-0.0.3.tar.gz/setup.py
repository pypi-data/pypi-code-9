import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "dockdev",
    version = "0.0.3",
    author = "Ian Maddison",
    author_email = "ian.maddison@digital.cabinet-office.gov.uk",
    description = ("A simple setup tool for docker containerized docker microservices"),
    license = "MIT",
    keywords = "docker container python development setup",
    url = "http://packages.python.org/dockdev",
    packages=['dockdev'],
    scripts=['bin/dockdev'],
    install_requires=['blessings', 'PyYAML', 'pystache'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)