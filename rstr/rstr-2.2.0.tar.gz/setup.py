from setuptools import setup

classifiers = [
 'Intended Audience :: Developers',
 'License :: OSI Approved :: BSD License',
 'Operating System :: OS Independent',
 'Programming Language :: Python :: 2.6',
 'Programming Language :: Python :: 2.7',
 'Programming Language :: Python :: 3.3',
 'Programming Language :: Python :: 3.4',
 'Topic :: Software Development :: Testing',
]


setup(name='rstr',
      version='2.2.0',
      description='Generate random strings in Python',
      author='Leapfrog Direct Response LLC',
      author_email='oss@leapfrogdevelopment.com',
      maintainer='Brendan.McCollam',
      maintainer_email='brendan@mccoll.am',
      license='BSD',
      platform='POSIX, MacOS, Windows, BeOS, PalmOS.',
      classifiers=classifiers,
      keywords=['Random strings',
                'random',
                'strings',
                'reverse regular expression'],
      url='http://bitbucket.org/leapfrogdevelopment/rstr/overview',
      packages=['rstr'],
      test_suite='rstr.tests.suite',
      )
