import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGELOG = open(os.path.join(here, 'CHANGELOG.rst')).read()

requires = []

setup(name='nvlib',
      version='1.0',
      description='nVentory library',
      long_description=README + '\n\n' + CHANGELOG,
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Intended Audience :: System Administrators ",
        ],
      author='Jesse Escobedo',
      author_email='jesse.escobedo@citygridmedia.com',
      url='',
      license='Apache',
      keywords='nvlib inventory cgm devops',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite='nose.collector',
      )
