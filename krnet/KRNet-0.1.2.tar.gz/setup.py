from distutils.core import setup

setup(
    # Application name:
    name="KRNet",
    # Version number (initial):
    version="0.1.2",
    # Application author details:
    author="Sanket Desai",
    author_email="desai.sanket12@gmail.com",
    # Packages
    packages=["krnet"],
    # Details
    url="https://pypi.python.org/pypi/KRNet",
    license="MIT",
    description="Constructs a metabolic network (NetworkX object) of KEGG reaction set.",
    long_description=open("README.md").read(),
    # Dependent packages (distributions)
)
