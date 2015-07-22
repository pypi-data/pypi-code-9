from setuptools import setup

setup(name='resin',
      version='0.1.2',
      description='Thin wrapper for resin api[work in progress]',
      url='http://github.com/craig-mulligan/resin-python-api-wrapper',
      author='craig-mulligan',
      author_email='craig@resin.io',
      license='MIT',
      packages=['resin'],
      install_requires = [
        'requests',
      ],
      zip_safe=False)
