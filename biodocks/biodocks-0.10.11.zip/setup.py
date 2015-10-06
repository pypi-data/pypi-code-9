from setuptools import setup

setup(name='biodocks',
      version='0.10.11',
      description='Pyqtgraph based widgets for image analysis',
      url='http://github.com/brettjsettle/BioWidgets',
      author='Brett Settle',
      author_email='brettjsettle@gmail.com',
      license='UCI',
      packages=['BioDocks', 'BioDocks.Widgets', 'BioDocks.io'],
      install_requires=['pyqtgraph', 'xlrd', 'pyopengl'],
      zip_safe=False)
