from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='commandRunner',
      version='0.3.0',
      description='Allows object oriented running of code/commands',
      long_description=readme(),
      url='https://github.com/AnalyticsAutomated/commandRunner.git',
      author='Analytics Automated',
      author_email='daniel.buchan@ucl.ac.uk',
      license='GPL',
      packages=['commandRunner'],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],
      )
