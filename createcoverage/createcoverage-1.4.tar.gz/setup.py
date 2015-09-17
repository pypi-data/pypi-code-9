from setuptools import setup

version = '1.4'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CREDITS.rst').read(),
    open('CHANGES.rst').read(),
    ])

install_requires = [
    'setuptools',
    'coverage >= 3.4',
    ],

tests_require = [
    ]

setup(name='createcoverage',
      version=version,
      description="Single command to create coverage reports (assumes a bin/test)",
      long_description=long_description,
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Development Status :: 6 - Mature",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Topic :: Software Development :: Libraries :: Python Modules",
          ],
      keywords=["testing", "coverage"],
      author='Reinout van Rees',
      author_email='reinout@vanrees.org',
      url='https://github.com/reinout/createcoverage',
      license='GPL',
      packages=['createcoverage'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require = {'test': tests_require},
      entry_points={
          'console_scripts': [
              'createcoverage = createcoverage.script:main',
              # Hack to make sure bin/coverage exists when we don't otherwise
              # explicitly tell buildout to create the script for this.
              'coverage = coverage:main',
          ]},
      )
