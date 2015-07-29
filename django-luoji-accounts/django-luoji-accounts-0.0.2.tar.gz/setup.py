import os
from setuptools import setup
from setuptools import find_packages

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(BASE_DIR, 'README.md')).read()
CHANGES = open(os.path.join(BASE_DIR, 'CHANGES.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(name='django-luoji-accounts',
      version='0.0.2',
      description='A general account app for projects',
      long_description=README + '\n\n' + CHANGES,
      author='Haotong Chen',
      author_email='hereischen@gmail.com',
      url='https://github.com/hereischen/django-luoji-accounts',
      license='BSD License',
      packages=['accounts'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 2.7',
      ],
      include_package_data=True,
      zip_safe=False,
      # test_suite='accounts.tests'
      )
