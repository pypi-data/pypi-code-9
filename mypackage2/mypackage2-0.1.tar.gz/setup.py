from distutils.core import setup
setup(
  name = 'mypackage2',
  packages = ['mypackage2'], # this must be the same as the name above
  version = '0.1',
  description = 'A random test lib',
  author = 'Vishwali Mhasawade',
  author_email = 'mvishwali28@gmail.com',
 # url = 'https://github.com/peterldowns/mypackage', # use the URL to the github repo
  #download_url = 'https://github.com/peterldowns/mypackage/tarball/0.1', # I'll explain this in a second
  keywords = ['testing', 'logging', 'example'], # arbitrary keywords
  classifiers = [],
)