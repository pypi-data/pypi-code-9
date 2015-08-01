from setuptools import setup

setup(name='randbanner',
      version='1.0.1',
      description='Random banner generator with colour support.',
      author='Jai Grimshaw',
      url='https://github.com/Jaiz909/randbanner/',
      author_email='randbanner@jaigrimshaw.com',
      license='MIT',
      install_requires=[
          'clint',
          'pyfiglet',
      ],
      scripts=['bin/randbanner'])
