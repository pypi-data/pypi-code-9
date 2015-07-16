from applause import __program_name__, __version__
from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.rst")).read()


install_requires = [
    "requests==2.6.0",
    "enum34==1.0.4",
    "click==4.0",
    "six==1.9.0"
]

setup(
    name=__program_name__,
    version=__version__,
    description="This package allows integration with Applause Inc. services.",
    long_description=README,
    classifiers=[
        # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Topic :: Utilities",
        "Topic :: System :: Shells",
        "Topic :: System :: Software Distribution",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
    ],
    keywords="",
    author="Applause Team",
    author_email="eng.warsaw@applause.com",
    url="",
    license="MIT",
    packages=find_packages(),
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        "console_scripts":
            ["applause-tool=applause.__main__:main"]
    }
)
