#!/usr/bin/env python
from distutils.core import setup

setup(name='boolfab',
      version='0.0.2',
      description='Boolfab: override fabric Task so it handles arguments as bool.',
      author='Julien Aubert',
      author_email='julien.aubert.mail@gmail.com',
      url='https://github.com/julienaubert/boolfab',
      keywords='fabric utilities',
      packages=['boolfab'],
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Topic :: Utilities",
          "License :: OSI Approved :: MIT License",
      ],
     )