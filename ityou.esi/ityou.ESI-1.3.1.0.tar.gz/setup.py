from setuptools import setup, find_packages
import os

version = '1.3.1.0'

setup(name='ityou.ESI',
      version=version,
      description="ITYOU ESI - A Social Intranet Solution based on Plone",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='Social Intranet, Plone, Activity Stream, Instant Messaging, Who is Online',
      author='ITYOU/LM',
      author_email='lm@ityou.de',
      url='http://www.ityou.de/esi',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ityou'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'ityou.esi.theme>=1.3.1,<2.0.0',
        'ityou.esi.viewlets>=1.3.1,<2.0.0',
        'ityou.jsonapi>=1.3.1,<2.0.0',
        'ityou.whoisonline>=1.3.1,<2.0.0',
        'ityou.extuserprofile>=1.3.1,<2.0.0',
        'ityou.astream>=1.3.1,<2.0.0',
        'ityou.imessage>=1.3.1,<2.0.0',
        'ityou.dragdrop>=1.3.1,<2.0.0',
        'ityou.thumbnails>=1.3.1,<2.0.0',
        'ityou.follow>=1.3.1,<2.0.0',
        'ityou.notify>=1.3.1,<2.0.0',
        'ityou.workflow>=1.3b2,<2.0.0',
        #'ityou.portlets>=1.3b1,<2.0.0',
        #'ityou.qrcode',
        'solgema.fullcalendar',
        'webcouturier.dropdownmenu',
        'sqlalchemy',
        'redis',
        'hiredis',
        'psycopg2',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      #setup_requires=["PasteScript"],
      #paster_plugins=["ZopeSkel"],
      )
