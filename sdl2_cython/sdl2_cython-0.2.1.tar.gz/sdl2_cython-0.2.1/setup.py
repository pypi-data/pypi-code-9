import os.path as pth
from setuptools import setup

# Function for reading text files
def _read(file_name):
    return open(pth.join(pth.dirname(__file__), file_name)).read()

# Run setup
setup(name='sdl2_cython',
      version='0.2.1',
      license=_read('LICENSE.txt'),
      description='Cython PXD files for SDL2',
      long_description=_read('README.rst'),
      author='Tim Jones',
      author_email='tgjonesuk@gmail.com',
      url='http://bitbucket.org/tgjones/sdl2_cython',
      keywords = ['sdl', 'sdl2', 'cython', 'pyx', 'pxd'],
      packages=['sdl2'],
      include_package_data=True)
