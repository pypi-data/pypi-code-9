# -*- coding: utf-8 -*-
from distutils.core import setup

setup(name='nxbimatch',
      version='0.20130323',
      py_modules=['bimatch'],
      description='generation of matchings in bipartite graphs',
      long_description="""
      The nxbimatch package is for generation of matchings in bipartite graphs.
      The prefix "nx" means that the package is based on NetworkX.""",
      author="MATSUI Tetsushi",
      author_email="VED03370@nifty.ne.jp",
      url="https://bitbucket.org/mft/nxbimatch/",
      classifiers=[
          "Development Status :: 4 - Beta",
          "License :: OSI Approved :: BSD License",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Intended Audience :: Science/Research",
          "Topic :: Scientific/Engineering :: Mathematics",
      ],
      install_requires=["networkx >= 1.7"],
      )

