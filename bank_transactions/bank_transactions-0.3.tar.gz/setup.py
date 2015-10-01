from setuptools import setup

setup(name='bank_transactions',
      version='0.3',
      install_requires=['nose'],
      description='Python package for importing bank transaction files.',
      url='https://github.com/henkvanramshorst/bank_transactions',
      author='Henk van Ramshorst',
      author_email='henk@vanramshorst.nl',
      license='MIT',
      packages=['bank_transactions'],
      zip_safe=False)