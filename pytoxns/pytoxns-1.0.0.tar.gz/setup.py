from distutils.core import setup
setup(
  name = 'pytoxns',
  packages = ['pytoxns'],
  version = '1.0.0',
  description = 'tox-dns for python',
  author = 'Drew DeVault',
  author_email = 'sir@cmpwn.com',
  url = 'https://github.com/SirCmpwn/pytoxns',
  download_url = 'https://github.com/SirCmpwn/pytoxns/tarball/1.0.0',
  keywords = ['tox', 'dns'],
  classifiers = [],
  requires = ['PyNaCl', 'cffi', 'dnslib', 'pycparser', 'six']
)
