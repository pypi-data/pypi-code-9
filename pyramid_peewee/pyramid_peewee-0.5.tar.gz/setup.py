import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'peewee',
    ]

setup(name='pyramid_peewee',
      version='0.5',
      description='Utilize Peewee as your ORM with Pyramid webapplications. - pyramid_peewee',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Framework :: Pyramid",
        "License :: OSI Approved :: MIT License",
        "Topic :: Database",
        ],
      author='Jose Galvez',
      author_email='jose@cybergalvez.com',
      url='https://bitbucket.org/jjgalvez/pyramid_peewee',
      download_url = 'https://bitbucket.org/jjgalvez/pyramid_peewee/get/0.5.zip',
      keywords='web pyramid pylons database peewee',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="pyramid_peewee.tests",
      entry_points="""
      """,
      )
