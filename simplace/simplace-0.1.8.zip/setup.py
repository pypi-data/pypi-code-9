'''
Created on 06.10.2015

@author: k
'''
from setuptools import setup
import sys
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


jp = 'Jpype1' if sys.version.startswith('2.') else 'Jpype1-py3'    

__version__ = ''
exec(open('simplace/_version.py').read())

setup(name='simplace',
      version=__version__,
      description='Interact with the simulation framework Simplace',
      long_description = """
Run and control simulations in the simulation framework Simplace.

You need Java >= 8.0 and the Simplace simulation framework http://www.simplace.net

To use it do::

    >>> import simplace
    >>> jd = 'd:/java/simplace/'
    >>> wd = 'd:/java/simplace/simplacerun/simulation/'
    >>> od = 'd:/java/simplace/simplacerun/output/'

    >>> sol = wd+'gk/solution/gecros/Gecros.sol.xml'
    >>> proj = wd+'gk/project/gecros/GecrosSensitivityTestNPL.proj.xml'
    
    >>> sh = simplace.initSimplace(jd,wd,od)
    >>> simplace.setProjectLines(sh, [1,3,8,9,17])
    >>> simplace.openProject(sh, sol, proj)
    >>> simplace.runProject(sh)
    >>> simplace.closeProject(sh)
      """,
      url='http://www.simplace.net/',
      author='Gunther Krauss',
      author_email='guntherkrauss@ui-bonn.de',
      license='GPL3',
      packages=['simplace'],
      install_requires=[
          jp,
      ],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering',
          'Programming Language :: Python',
          'Programming Language :: Java'
          
      ],
      zip_safe=False)