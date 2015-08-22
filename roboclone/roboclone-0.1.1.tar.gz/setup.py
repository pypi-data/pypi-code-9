import os
from setuptools import setup


def read(file):
    return open(os.path.join(os.path.dirname(__file__), file)).read()


setup(
    name="roboclone",
    version="0.1.1",
    packages=['roboclone'],
    author="Simon Andrews",
    url="https://github.com/simon-andrews/roboclone",
    description="A script for cloning FRC robot projects and configuring them for Eclipse",
    long_description=read("README.rst"),
    license="MIT",
    install_requires=['Jinja2'],
    scripts=['bin/roboclone'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Topic :: Utilities",
    ]
)
