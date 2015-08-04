import codecs
from setuptools import setup, find_packages
import os
import re


with codecs.open(os.path.join(os.path.abspath(os.path.dirname( __file__)), '__init__.py'), 'r', 'latin1') as fp:
    try:
        version = re.findall(r"^__version__ = '([^']+)'$", fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


def read(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read().strip()

install_requires = ['aiohttp', 'aiohttp_jinja2', 'aiohttp_debugtoolbar', 'pymongo']
#tests_require = install_requires + ['nose']


setup(name='tao1',
      version=version,
      description=("framework, CMS and CRM for aiohttp"),
#      lond_description='\n\n'.join((read('README.rst'), read('CHANGES.txt'))),
      classifiers=[
#          'License :: OSI Approved :: Lesser General Public License LGPLv2',
#          'License :: LGPLv2',
          'Intended Audience :: Developers',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Topic :: Internet :: WWW/HTTP'],
      author="Alexandre Z",
      author_email="alikzao@gmail.com",
      url='https://github.com/alikzao/tao',
      license='LGPLv2',
      packages=find_packages(),
      install_requires=install_requires,
#      tests_require=tests_require,
#      test_suite='nose.collector',
      include_package_data=True)
      
      
      
      
      
      