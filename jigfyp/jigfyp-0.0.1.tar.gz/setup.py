from distutils.core import setup

setup(name='jigfyp',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Index a leveldb with tuples',
      url='http://dada.pink/jigfyp/',
      packages=['jigfyp'],
      tests_require = [
          'pytest>=2.6.4', 'pytest-quickcheck>=0.8.2',
      ],
      version='0.0.1',
      license='LGPL',
)
