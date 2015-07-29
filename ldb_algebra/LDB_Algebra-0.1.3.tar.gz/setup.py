from setuptools import setup

setup(name='LDB_Algebra',
      version='0.1.3',
      description='An algebra/calculus package for the LDB framework',
      author='Alex Orange',
      author_email='alex@eldebe.org',
      packages=['ldb', 'ldb.algebra'],
      namespace_packages=['ldb'],
      url='http://www.eldebe.org/ldb/algebra/',
      license='AGPLv3',
      test_suite='test',
     )
