from setuptools import setup, find_packages
from congo import VERSION

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name = 'django-congo',
      version = VERSION.replace(' ', '-'),
      description = 'Some useful tool for faster and more efficient Django application development.',
      long_description = readme(),
      classifiers = [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords = 'congo django utils integree',
      url = 'http://www.integree.pl/',
      author = 'Integree Bussines Solutions',
      author_email = 'dev@integree.pl',
      license = 'MIT',
      packages = find_packages(),
      install_requires = [
          'django<1.9',
      ],
      include_package_data = True,
      zip_safe = False)
