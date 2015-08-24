from setuptools import setup, find_packages
import os

version = '1.0.0'

tests_require = [
    'unittest2',
]


setup(name='ftw.autofeature',
      version=version,
      description="ftw.autofeature automatically registers ZCML features.",
      long_description=open("README.rst").read() + "\n" + open(
          os.path.join("docs", "HISTORY.txt")).read(),

      classifiers=[
          "Environment :: Web Environment",
          'Framework :: Plone',
          'Framework :: Plone :: 4.3',
          "Intended Audience :: Developers",
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],

      keywords='ftw autofeature zcml feature',
      author='4teamwork AG',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/ftw.autofeature',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
          'path.py',
          'setuptools',
          'zope.configuration',
          'zope.interface',
      ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require,
                          example=['unittest2']),

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """)
