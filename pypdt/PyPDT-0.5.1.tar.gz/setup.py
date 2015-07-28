#! /usr/bin/env python

from distutils.core import setup

## Setup definition
import pypdt
__doc__ = pypdt.__doc__

setup(name = 'PyPDT',
      version = pypdt.__version__,
      packages = ["pypdt"],
      author = 'Andy Buckley',
      author_email = 'andy@insectnation.org',
      #url = 'http://www.insectnation.org/projects/pypdt',
      description = 'Pythonic access to high energy particle data tables and PDG ID codes.',
      long_description = __doc__,
      scripts=["pdt"],
      data_files=[("share/pypdt", ["mass_width_2014.mcd"])],
      keywords = 'hep physics particle mass lifetime charge pid pdg ctau montecarlo',
      license = 'GPL')
