from setuptools import setup

setup(name='govtrack2csv',
      version='1.0',
      description='Toolset for converting govtrack data to csv.',
      url='http://github.com/hackthefed/govtrack2csv',
      author='Hack The Fed',
      author_email='vance@hackthefed.com',
      license='MIT',
      packages=['govtrack2csv'],
      scripts=['bin/convert_congress'],
      install_requires=[
          'pandas',
          'pyyaml',
          'numpy'
      ],
      zip_safe=False)
