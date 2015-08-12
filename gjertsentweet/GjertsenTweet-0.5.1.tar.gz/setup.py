__author__ = 'Fredrik Gjertsen'
__doc__ = open('README.rst').read()
__description__ = 'A simple twitter client for the command line'
__version__ = '0.5.1'

from setuptools import setup

setup(name='GjertsenTweet',
      version=__version__,
      description=__description__,
      long_description = __doc__,
      author=__author__,
      author_email='f.gjertsen@gmail.com',
      url='https://github.com/fredgj/GjertsenTweet',
      packages=['GjertsenTweet'],
      license='GNU General Public License',
      install_requires=['npyscreen==4.9.1',
                        'twitter==1.17.0',
                        'dict-digger==0.2.1'],
      entry_points={
          'console_scripts':
            ['gjertsentweet=GjertsenTweet.client:main',
             'GjertsenTweet=GjertsenTweet.client:main']
          },
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Environment :: Console :: Curses',
                   'Intended Audience :: End Users/Desktop',
                   'Natural Language :: English',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 2 :: Only',
                   'Programming Language :: Python :: Implementation :: CPython',
                   'Topic :: Communications',
                   'Topic :: Internet',
                   'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
                   'Topic :: Utilities',
                   'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                   ],
      keywords='twitter, command-line tools')


