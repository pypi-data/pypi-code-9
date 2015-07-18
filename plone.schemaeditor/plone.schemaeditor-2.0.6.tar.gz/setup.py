from setuptools import setup, find_packages

version = '2.0.6'

setup(name='plone.schemaeditor',
      version=version,
      description="Provides through-the-web editing of a zope schema/interface.",
      long_description=open("README.rst").read() + "\n" +
      open("CHANGES.rst").read(),
      classifiers=[
          "Framework :: Zope2",
          "Framework :: Plone",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "License :: OSI Approved :: BSD License",
      ],
      keywords='plone schema ttw',
      author='David Glick',
      author_email='dglick@gmail.com',
      url='http://svn.plone.org/svn/plone/plone.schemaeditor',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Zope2',
          'zope.cachedescriptors',
          'zope.component',
          'zope.container',
          'zope.globalrequest',
          'zope.interface',
          'zope.lifecycleevent',
          'zope.schema',
          'zope.publisher',
          'z3c.form',
          'plone.z3cform',
          'plone.autoform',
      ],
      extras_require={'test': [
          'plone.app.dexterity',
          'plone.app.testing',
          'plone.app.robotframework',
      ]},
      )
