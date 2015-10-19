from distutils.core import setup
setup(
  name = 'zohoautomate',
  packages = ['zohoautomate'], # this must be the same as the name above
  version = '0.0.2',
  description = '''A library to do basic operations in Zoho Mail, as they don't provide an API.''',
  author = 'Tom Werner',
  author_email = 'hello.github@tomwerner.me.uk',
  url = 'https://github.com/tomwerneruk/zohoautomate', # use the URL to the github repo
  download_url = 'https://github.com/tomwerneruk/zohoautomate/tarball/v0.0.2', # I'll explain this in a second
  keywords = ['zoho', 'api', 'automation', 'mail'], # arbitrary keywords
  setup_requires =[
    'selenium',
  ]
)