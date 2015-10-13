from setuptools import setup

setup(name='ds_utils',
      version='0.3.1',
      description='Utilities for Hudl Data Science',
      long_description='Utilities used by the Data Science Squad at Hudl.'
                       'Includes a wrapper for Amazon Kinesis that provides easy logging'
                       'and a utility to provide information (ROC, etc.) about binary classifiers.',
      author='Hudl Data Science Squad',
      url='http://hudl.github.io/',
      author_email='',
      maintainer='Nathan DeMaria',
      maintainer_email='nathan.demaria@hudl.com',
      license='MIT',
      install_requires=[
          'boto',
          'pandas',
          'numpy',
          'matplotlib',
          'scikit-learn',
          'pylab'
      ],
      packages=['ds_classifier', 'ds_logger'],
      entry_points={}
      )
