from distutils.core import setup

classifiers = ['Intended Audience :: Developers']

setup(name='Gremlins',
      version='0.0.1',
      author='Robert Escriva (rescrv)',
      author_email='robert@rescrv.net',
      packages=[],
      package_dir={},
      package_data={},
      scripts=['gremlin'],
      url='http://rescrv.net',
      license='3-clause BSD',
      description='Controlled chaos for testing.',
      long_description=open('README').read(),
      classifiers=classifiers,
      )
