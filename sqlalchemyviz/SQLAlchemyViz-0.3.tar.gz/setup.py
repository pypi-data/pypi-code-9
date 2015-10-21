from setuptools import setup
import os
# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='SQLAlchemyViz',
    version='0.3',
    packages=['sqlalchemyviz'],
    url='',
    license='MIT',
    author='Sebastian Eckweiler',
    author_email='seb.eckweiler@gmail.com',
    description='Package to create ER diagrams from SQLAlchemy schemas using Graphviz.',
    long_description=read('README.rst'),
    install_requires=['sqlalchemy', 'pydot'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Topic :: Database",
        "Topic :: Documentation",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python"
    ],
    entry_points={
        'console_scripts': [
            'sqlaviz = sqlalchemyviz.cli:main',
        ]
    }
)
