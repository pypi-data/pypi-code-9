from setuptools import setup

setup(name='LDB_Algebra',
      version='0.3.2',
      description='An algebra/calculus package for the LDB framework',
      author='Alex Orange',
      author_email='alex@eldebe.org',
      packages=['ldb', 'ldb.algebra'],
      namespace_packages=['ldb'],
      url='http://www.eldebe.org/ldb/algebra/',
      license='AGPLv3',
      extras_require={
          'implicit_differentiation': ['LDB_LAPACK'],
      },
      test_suite='test',
     )
