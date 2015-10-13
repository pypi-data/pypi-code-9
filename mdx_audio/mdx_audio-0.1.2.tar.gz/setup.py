import os
from distutils.core import setup
from mdx_audio import __version__, __author__


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as file_handle:
        return file_handle.read()


setup(name='mdx_audio',
      version=__version__,
      description='Markdown 2.0 extension for audio',
      long_description=read("README.rst"),
      author=__author__,
      author_email='panosktn@gmail.com',
      url='https://github.com/pgk/python-markdown-audio',
      py_modules = ['mdx_audio'],
)
