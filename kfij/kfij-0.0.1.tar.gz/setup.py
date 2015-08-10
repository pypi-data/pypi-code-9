from distutils.core import setup

setup(name='kfij',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Persist primative data structures to disk',
      url='https://github.com/tlevine/kfij',
      packages=['kfij'],
      tests_require = [
          'pytest>=2.6.4',
          'pytest-quickcheck>=0.8.2',
      ],
      version='0.0.1',
      license='LGPL',
)
