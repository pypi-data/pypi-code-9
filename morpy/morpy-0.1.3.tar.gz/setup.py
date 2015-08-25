import os
import numpy
from setuptools import find_packages
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

version = '0.1.3'
README = os.path.join(os.path.dirname(__file__), 'README.md')
long_description = open(README).read() + '\n'

cmdclass = { }
ext_modules = [ ]

cmdclass.update({ 'build_ext': build_ext })
ext_modules = [
    Extension("morpy.cmorton",
              sources=["morpy/cmorton.pyx"],
              include_dirs=[numpy.get_include()],
              extra_compile_args=["-std=c99"],
              )
]
install_requires = [
    'numpy>=1.9.0',
    'Cython >= 0.22',
]

setup(name='morpy',
      version=version,
      description=("Morton Curve Library"),
      long_description=long_description,
      cmdclass = cmdclass,
      ext_modules=ext_modules,
      install_requires=install_requires,
      classifiers=[
          "Programming Language :: Python",
          ("Topic :: Software Development :: Libraries :: Python Modules"),
      ],
      keywords=['space filling curve','morton'],
      author='Samuel Skillman <samskillman@gmail.com>',
      license='MIT',
      packages=find_packages(),
      )
