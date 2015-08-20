from setuptools import setup, find_packages

setup(name='pyripple',
      version='0.0.2',
      description='Python package for data analysis of the Ripple peer-to-peer network',
      url='http://github.com/gip/pyripple',
      author='Gilles Pirio',
      author_email='gilles.xrp@gmail.com',
      license='Apache License 2.0',
      packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
      zip_safe=False,
      install_requires= ['numpy', 'matplotlib', 'mpmath', 'pandas', 'websocket-client'])
