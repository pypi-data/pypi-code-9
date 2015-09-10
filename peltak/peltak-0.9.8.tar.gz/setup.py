import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = "peltak",
    version = "0.9.8",
    author = "Mateusz 'novo' Klos",
    author_email = "novopl@gmail.com",
    license = "MIT",
    keywords = "project management git gitlab",
    url = "http://github.com/novopl/peltak",
    entry_points={
        'console_scripts': [
            'peltak = peltak.runner:main'
        ]
    },
    packages=[
        'peltak',
        'peltak.actions',
        'peltak.common',
        'peltak.core',
        'peltak.system',
    ],
    description = ("Command line utility to improve your daily workflow."
                   "The main focus so far is making a gitlab merge request."),
    long_description=read('README.rst'),
    install_requires = [
        'six', 'libigor', 'requests'
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
    ],
)
