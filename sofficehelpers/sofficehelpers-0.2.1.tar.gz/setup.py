
import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='sofficehelpers',
    version='0.2.1',
    packages=['sofficehelpers'],
    entry_points={
        'console_scripts': [
            'ssconverter = sofficehelpers.ssconverter:main'
        ]
    },
    url='https://github.com/chintal/tendril-sofficehelpers',
    license='GNU LGPLv2.1+',
    author='Chintalagiri Shashank',
    author_email='shashank@chintal.in',
    description='Helpers for LibreOffice integration with automated tools',
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Programming Language :: Python :: 3.4",
        "Intended Audience :: Information Technology",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
    ],
)
