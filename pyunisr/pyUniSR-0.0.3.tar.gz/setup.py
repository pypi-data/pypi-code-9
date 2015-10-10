import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pyUniSR",
    version = "0.0.3",
    author = "Nicolo Balzarotti",
    author_email = "anothersms@gmail.com",
    description = ("Python class to access studenti.unisr.it (Univerity Vita-Salute San Raffaele, Milano)"),
    license = "GPLv2",
    keywords = "unisr class milano university raffaele",
    url = "https://github.com/nico202/pyUniSR",
    packages=['UniSR'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
)
