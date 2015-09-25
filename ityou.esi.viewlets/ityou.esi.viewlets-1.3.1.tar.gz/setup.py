from setuptools import setup, find_packages
import os

version = '1.3.1'

setup(name='ityou.esi.viewlets',
      version=version,
      description="ITYOU ESI viewlets",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),    
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='Social Intranet, Plone, viewlets',
      author='ITYOU/LM',
      author_email='lm@ityou.de',
      url='http://www.ityou.de/esi/',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['ityou', 'ityou.esi'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'ityou.esi.theme',
      ],
      extras_require={'test': ['plone.app.testing']},
      entry_points="""
      # -*- Entry points: -*-
  	  [z3c.autoinclude.plugin]
  	  target = plone
      """,
      #setup_requires=["PasteScript"],
      #paster_plugins=["ZopeSkel"],
      )
