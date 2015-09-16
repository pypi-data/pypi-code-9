#from ez_setup import use_setuptools
#use_setuptools()
#from setuptools import setup, find_packages
from distutils.core import setup
     
setup(
        name             = 'sdebug',
        version          = '1.1',
        maintainer       = 'Moreno Bonaventura',
        maintainer_email = 'morenobonaventura@gmail.com',
        author           = 'Moreno Bonaventura',
        author_email     = 'morenobonaventura@gmail.com',
        description      = 'simple debug to print on stderr',
        keywords         = 'debug sys stderr',
        license          = 'GNU2',
        packages         = ['sdebug'],
    ) 
      