from distutils.core import setup
setup(
  name = 'smsowl',
  packages = ['smsowl'], # this must be the same as the name above
  install_requires = ['requests'],
  version = '1.0.0',
  description = 'This is Python wrapper for SmsOwl REST API',
  author = 'M/s Mahoujas',
  author_email = 'mahoujas@mahoujas.com',
  url = 'https://github.com/mahoujas/smsowl-python', # use the URL to the github repo
  download_url = 'https://github.com/mahoujas/smsowl-python/tarball/1.0.0', # I'll explain this in a second
  keywords = ['SmsOwl', 'smsowl', 'transactional sms','promotional sms','sms india','sms gateway','dnd sms'], # arbitrary keywords
  classifiers = [],
)