import os
from setuptools import setup

#https://pythonhosted.org/an_example_pypi_project/setuptools.html
# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


install_requires = [
    'ipython' if os.name == 'posix' else 'ipython[terminal]',
    'hammock', 'pygments', 'docopt', 'pyyaml'
]

setup(
    name="iodine",
    version="0.0.2",
    author="Steven Joseph",
    author_email="steven@stevenjoseph.in",
    description="A salt-api client based on IPython",
    license="BSD",
    keywords="salt saltstack client ipython",
    url="http://packages.python.org/iodine",
    packages=['iodine'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
        ],
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'iodine = iodine.__main__:main'
        ]
    },
)
