from setuptools import setup, find_packages
import os

version = '1.0.0'

setup(name='edeposit.policy',
      version=version,
      description="E-Deposit Policy",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Jan Stavel',
      author_email='stavel.jan@gmail.com',
      url='https://github.com/edeposit/edeposit.policy',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['edeposit'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'Plone',
          'plone.namedfile',
          'Products.PloneFormGen',
          'plone.app.dexterity',
          'edeposit.content',
          'edeposit.user',
          'edeposit.theme',
          'plone.api',
      ],
      extras_require = {
          'test': ['plone.app.testing',]
      },
      entry_points="""
 # -*- Entry points: -*-

 [z3c.autoinclude.plugin]
 target = plone""",
      # setup_requires=["PasteScript"],
      # paster_plugins=["ZopeSkel"],
      )
