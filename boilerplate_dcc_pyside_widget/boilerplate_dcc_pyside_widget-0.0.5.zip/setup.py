
# Import
# ------------------------------------------------------------------
from setuptools import setup
from setuptools import find_packages

# Setup
# ------------------------------------------------------------------
setup(name='boilerplate_dcc_pyside_widget',
      version='0.0.5',
      description='Repository for boilerplate PySide DCC widget. This tool serves as barebone,\
      fully functional skeleton for DCC GUI tools written in PySide.',
      url='http://timmwagener.com/',
      author='Timm Wagener',
      author_email='wagenertimm@gmail.com',
      license='MIT',
      keywords='PySide DCC Maya Nuke Timm Wagener',
      packages=find_packages(),
      include_package_data=True,
      classifiers=['Programming Language :: Python',
                      'Topic :: Software Development',],
      zip_safe = False)
