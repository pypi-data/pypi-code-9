from setuptools import setup
from setuptools import find_packages

version = __import__('pelican_vidme').__version__
download_url = 'https://github.com/chriscowley/pelican_vidme/archive/{}.zip'.format(version)

setup(name='pelican_vidme',
      version=version,
      url='https://github.com/chriscowley/pelican_vidme',
      download_url=download_url,
      author="Chris Cowley",
      author_email="chris@chriscowley.me.uk",
      maintainer="Chris Cowley",
      maintainer_email="chris@chriscowley.me.uk",
      description="Easily embed Vidme videos in your posts",
      long_description=open("README.rst").read(),
      license='MIT',
      platforms=['linux'],
      packages=find_packages(exclude=["*.tests"]),
      package_data={'': ['LICENSE', ]},
      install_requires = ['pelican'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.1',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: Implementation :: CPython',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Text Processing',
      ],
      zip_safe=True,
      )
