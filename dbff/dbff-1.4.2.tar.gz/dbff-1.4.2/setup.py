from setuptools import setup, find_packages

PACKAGE = "dbff"
NAME = "dbff"
VERSION = __import__(PACKAGE).__version__

setup(name=NAME,
      version=VERSION,
      author="Xiayi Li",
      author_email="hi@xiayi.li",
      url="https://github.com/yosg/dbff",
      packages=find_packages(),
      description="Compare tables and rows between MySQL databases.",
      license="MIT License",
      install_requires=["MySQL-python"]
)
