from setuptools import setup

setup(name='os0',
      version='0.2.6',
      description='OS indipendent interface',
      long_description="""
Manage both URI both local filenames.
""",
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: GNU Affero General Public License v3',
          'Programming Language :: Python :: 2.6',
          'Intended Audience :: Developers',
          'Topic :: Software Development',
          'Topic :: Software Development :: Build Tools',
          'Operating System :: OS Independent',
      ],
      keywords='os path linux windows openvms',
      url='http://wiki.zeroincombenze.org/en/Python/opt/os0',
      author='Antonio M. Vigliotti',
      author_email='antoniomaria.vigliotti@gmail.com',
      license='Affero GPL',
      packages=['os0'],
      zip_safe=False)
