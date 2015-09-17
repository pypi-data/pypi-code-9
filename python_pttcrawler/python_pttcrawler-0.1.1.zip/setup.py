__author__ = 'Vetom'

from setuptools import setup

setup(name='python_pttcrawler',
      version='0.1.1',
      description='Data Lab API for Python',
      author='Patrick Yeh',
      author_email='vetom198@gmail.com',
      install_requires=['requests','BeautifulSoup'],
      url='https://github.com/patrickyeh/python-pttcrawler',
      packages=['python_pttcrawler'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7']
      )
