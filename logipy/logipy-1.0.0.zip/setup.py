import os
from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name = "logipy",
    version = "1.0.0",
    author = "Tom Lambert",
    author_email = "devtechsupport@logitech.com",
    description = ("A simple python wrapper for Logitech G's LED and Arx SDKs."),
    long_description = long_description,
    keywords = ["logi", "logipy", "Logitech", "LogitechG", "LED", "Arx", "LGS", "Logitech Gaming Software"],
    url = "http://gaming.logitech.com/en-us/developers",
	download_url = "https://github.com/Logitech/logiPy/tarball/master",
    packages=['logipy'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Libraries",
    ],
)