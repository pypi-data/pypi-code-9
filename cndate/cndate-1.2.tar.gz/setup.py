# coding:utf-8
"""
setup(
    name="MyLibrary",
    version="1.0",
    install_requires=[
        "requests",
        "bcrypt",
    ],
    # ...
)
"""
from distutils.core import setup

setup(name='cndate',
      version='1.2',
      packages=['cndate'],
      install_requires=[
            "dateutils",
      ],
      )