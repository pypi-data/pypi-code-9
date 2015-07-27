import os
from renderconf import VERSION
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='renderconf',
    version=VERSION,
    author='Matthew Wedgwood',
    author_email='mwedgwood@gmail.com',
    description=('A tool for rendering templated configuration files from a '
                 'variety of data sources'),
    license='MIT',
    keywords=['configuration', 'docker', 'templating'],
    url = 'http://github.com/slank/renderconf',
    packages=[
        'renderconf',
        'renderconf.backends',
    ],
    #  long_description=read('README.md'),
    install_requires=[
        'Jinja2==2.8',
        'requests==2.7.0',
    ],
    entry_points={
        'console_scripts': [
            'renderconf=renderconf.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
    ],
)
