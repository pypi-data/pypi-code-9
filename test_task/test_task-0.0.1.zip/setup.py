
"""
test_task
==========================================

Package prepared as barebone skeleton for an
application.
"""

# Import
# ------------------------------------------------------------------
from setuptools import setup
from setuptools import find_packages

# Setup
# ------------------------------------------------------------------
setup(name='test_task',
      version='0.0.1',
      description='Package prepared as barebone skeleton for an application',
      url='https://github.com/timmwagener',
      author='Timm Wagener',
      author_email='wagenertimm@gmail.com',
      license='MIT',
      keywords='Python Package Skeleton',
      packages=find_packages(),
      include_package_data=True,
      classifiers=['Programming Language :: Python',],
      zip_safe=False)
