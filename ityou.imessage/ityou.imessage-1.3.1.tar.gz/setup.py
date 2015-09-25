from setuptools import setup, find_packages
import os

version = '1.3.1'

setup(name='ityou.imessage',
      version=version,
      description="Instant Messaging for ITYOU ESI",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='Messaging',
      author='ITYOU/LM',
      author_email='lm@ityou.de',
      url='http://www.ityou.de/esi/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ityou'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'ityou.esi.theme',
          'sqlalchemy',
          'stripogram',
          'BeautifulSoup',
          'psycopg2'
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      #setup_requires=["PasteScript"],
      #paster_plugins=["ZopeSkel"],
      )

