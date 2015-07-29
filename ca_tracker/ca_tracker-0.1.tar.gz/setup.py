from setuptools import setup

setup(name='ca_tracker',
      version='0.1',
      description='Package for cell segmentation, tracking, classification into asc negative and asc positive cells and calcium intensity measurements over time',
      #url='http://github.com/storborg/funniest',
      author='Christoph Moehl, Image and Data Analysis Facility, German Center of Neurodegenerative Diseases, Bonn, Germany',
      author_email='christoph.moehl@dzne.de',
      #license='MIT',
      packages=['ca_tracker'],
      install_requires=['image', 'matplotlib==1.3.1', 'numpy', 'pandas', 'python-dateutil', 'scikit-image', 'scipy', 'seaborn'],
      test_suite = 'nose.collector',
      tests_require = ['nose'],
      scripts = ['bin/ca_tracker_2', 'bin/ca_tracker_1'],
      zip_safe=False)
