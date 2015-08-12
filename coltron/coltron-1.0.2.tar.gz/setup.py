from setuptools import setup, find_packages

def readme():
    """Returns file object of the readme file"""
    with open('README.rst') as f:
        return f.read()

package_name = 'coltron'
version = '1.0.2'
description = 'Package for generating and analyzing transcription networks'
long_description = readme()

url = 'https://github.com/BradnerLab/pipeline'
author = 'Alex Federation'
author_email = 'drpolaskijr@gmail.com'
packages = find_packages()

requires = ['networkx','numpy']
keywords = "transcription regulatory networks bradner"

# Setting entry points will build a script for the main function from CRC
entry_points={'console_scripts':['coltron = coltron.crc:main', 
                                 'coltron-get-data = coltron.crc:downloadDataFiles']}
package_data = {"":["data/annotation/*ucsc", "data/annotation/*txt"]}

setup(name=package_name,
      version=version,
      url=url,
      author=author,
      author_email=author_email,
      install_requires=requires,
      entry_points = entry_points,
      requires = requires,
      packages=packages,
      package_data=package_data,
      long_description=long_description,
      description = description
)
