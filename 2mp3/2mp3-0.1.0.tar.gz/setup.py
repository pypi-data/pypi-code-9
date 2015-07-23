from distutils.core import setup

setup(
    # Application name:
    name="2mp3",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="komuW",
    author_email="komuw05@gmail.com",

    # Packages
    packages=["2mp3"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="http://pypi.python.org/pypi/2mp3_v010/",

    #
    # license="LICENSE.txt",
    description="convert your media files to mp3",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "envoy",
    ],
)