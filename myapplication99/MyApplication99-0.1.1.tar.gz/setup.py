from distutils.core import setup

setup(
    # Application name:
    name="MyApplication99",

    # Version number (initial):
    version="0.1.1",

    # Application author details:
    author="name surname",
    author_email="name@addr.ess",

    # Packages
    packages=["app"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="http://pypi.python.org/pypi/MyApplication_v011/",

    #
    # license="LICENSE.txt",
    description="first sj sample by rp",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "flask",
    ],
)
