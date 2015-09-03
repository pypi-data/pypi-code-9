from codecs import open as codecs_open
from setuptools import setup
import pln


# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(name='pln',
      version=pln.__version__,
      description='A library to apply successive operations on your data.',
      long_description=long_description,
      classifiers=[],
      keywords='',
      author=pln.__author__,
      author_email=pln.__email__,
      url='https://github.com/TaurusOlson/pln',
      license=pln.__version__,
      packages=['pln'],
      include_package_data=True,
      zip_safe=False
      )
