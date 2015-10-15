from setuptools import setup, find_packages

setup(name='SlowTests',
      entry_points={
          'nose.plugins.0.10': [
              'slowtests= slow_tests:SlowTests'
          ]
      },
      packages=find_packages(),
      install_requires=['nose'],
      version="0.0.2",
      license="MIT License",
      author="Yellowbeard",
      author_email="artbasher@gmail.com",
      url="https://github.com/yellow-beard/slow_tests",
      description="Plugin for noset that identifies and prints your slowest tests"
      )

