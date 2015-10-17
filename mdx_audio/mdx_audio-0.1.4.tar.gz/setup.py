from distutils.core import setup
from mdx_audio import __version__, __author__


setup(name='mdx_audio',
      version=__version__,
      description='Markdown 2.0 extension for audio',
      author=__author__,
      author_email='panosktn@gmail.com',
      url='https://github.com/pgk/python-markdown-audio',
      py_modules = ['mdx_audio'],
)
