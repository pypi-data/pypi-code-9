from setuptools import setup, find_packages

setup(name='giwyn',
      version='0.3.1',
      packages=find_packages(),
      description='A simple command to manage all your git clones',
      url='http://github.com/k0pernicus/giwyn',
      author='k0pernicus',
      author_email='antonin.carette@gmail.com',
      license='GnuGPL',
      classifiers=[
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'Programming Language :: Python :: 3.4',
          'Environment :: Console',
      ],
      keywords='git development versioning package',
      install_requires=[
        'gitpython',
      ],
      entry_points={
        'console_scripts': [
            'giwyn=giwyn.main:main'
        ]
      })
