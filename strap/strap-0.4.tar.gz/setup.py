#!/usr/bin/env python

#
# (c)2005 LIRIS - University Claude Bernard Lyon 1
# http://liris.cnrs.fr/
#
# Author: Pierre-Antoine CHAMPIN
# http://champin.net/
#
# This software is distributed under the terms of the GNU LGPL v2.1.
# See LICENSE.txt for more details.
#

try:
    from setuptools import setup
except:
    from distutils.core import setup

from strap import PACKAGE_VERSION

setup(name =        'strap',
      version =     PACKAGE_VERSION,
      description = 'Simple sTreamed Rdf Access Protocol',
      author =      'Pierre-Antoine Champin',
      author_email ='strap@champin.net',
      url =         'http://champin.net/dev/strap/',

      packages = [
        'strap',
        'strap.rdflib_impl',
      ],
      long_description = """Strap is a protocol for exchanging RDF graphs between independant software
components.  Rather than using standard serialization syntaxes, Strap
transports RDF graphs as a stream of triples which can be interrupted at any
moment.""",
      keywords = "rdf semantic-web component rdflib",
      license="GNU LGPL v2.1",
      platforms="All",

    # egg specific
        extras_require = {
            'rdflib': ["rdflib>=2.2.1"],
        },

     )
