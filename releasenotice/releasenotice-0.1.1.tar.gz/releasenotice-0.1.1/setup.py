import sys

try:
    from setuptools import setup
except:
    try:
        from distutils.core import setup
    except:
        print "Couldn't use either setuputils or distutils. Install one of those."
        sys.exit(1)

requires = ['slacker>=0.7.0']

if sys.version_info < (2, 7):
    requires.append('argparse')

setup(name='releasenotice',
      version="0.1.1",
      license="Apache 2'",
      install_requires=requires,
      description='A tool for automated release announcement to Slack chat.',
      author='Dell Software Inc',
      author_email='ian.gable@software.dell.com',
      url='https://github.com/igable/releasenotice',
      scripts=['releasenotice'],
      data_files=[('share/releasenotice', ['releasenotice.conf'])],
      )
