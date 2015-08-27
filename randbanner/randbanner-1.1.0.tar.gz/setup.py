from setuptools import setup, find_packages

setup(name='randbanner',
      version='1.1.0',
      description='Random banner generator with colour support.',
      author='Jai Grimshaw',
      url='https://github.com/Jaiz909/randbanner/',
      author_email='randbanner@jaigrimshaw.com',
      license='MIT',
      install_requires=[
          'clint',
          'pyfiglet',
      ],
      packages=find_packages(),
      entry_points={
         'console_scripts': [
         'randbanner = randbanner.randbanner:main',
         ],
      },)
