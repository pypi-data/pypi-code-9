from distutils.core import setup
setup(
  name = 'packers',
  packages = ['pack', 'pack.packchild'], # this must be the same as the name above
  version = '0.1',
  description = 'A random lib',
  author = 'Akshar Raaj',
  author_email = 'akshar@agiliq.com',
  url = 'https://github.com/akshar-raaj/mypackage', # use the URL to the github repo
  download_url = 'https://github.com/akshar-raaj/mypackage/tarball/0.1', # I'll explain this in a second
  keywords = ['testing', 'example'], # arbitrary keywords
  classifiers = [],
)