from setuptools import setup, find_packages
import os

version = '1.3'
long_description = open("README.rst").read()
long_description += "\n"
long_description += open(os.path.join(
    "collective", "depositbox", "usage.rst")).read()
long_description += "\n"
long_description += open("CHANGES.rst").read()

setup(name='collective.depositbox',
      version=version,
      description="Put stuff in a box, get it out again with the secret",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Framework :: Plone :: 3.3",
          "Framework :: Plone :: 4.0",
          "Framework :: Plone :: 4.1",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
          "Framework :: Plone :: 5.0",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.4",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          ],
      keywords='anonymous secret',
      author='Maurits van Rees',
      author_email='maurits@vanrees.org',
      url='https://github.com/collective/collective.depositbox',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
