from setuptools import setup, find_packages

version = '0.1.0'

setup(name='anybox.scripts.odoo',
      version=version,
      description="Import CSV Odoo scripts",
      long_description=""" """,
      classifiers=[],
      author=u'Jean-Sébastien Suzanne',
      author_email='jssuzanne@anybox.fr',
      url='',
      license='',
      namespace_packages=['anybox', 'anybox.scripts'],
      packages=find_packages('.',
                             exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'setuptools',
          'argparse',
      ],
      entry_points="""
      [console_scripts]
      import_csv=anybox.scripts.odoo.import_csv:run
      """,
      )
