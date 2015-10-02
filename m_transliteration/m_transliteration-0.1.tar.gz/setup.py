from distutils.core import setup
import os
os.system('cp transliteration /usr/bin')
os.system('mkdir $HOME/.m_transliteration')
setup(
  name = 'm_transliteration',
  packages = ['m_transliteration'], # this must be the same as the name above
  version = '0.1',
  description = 'English-Marathi transliteration',
  author = 'PICT',
  author_email = 'mvishwali28@gmail.com',
  #url = 'https://github.com/peterldowns/mypackage', # use the URL to the github repo
  #download_url = 'https://github.com/peterldowns/mypackage/tarball/0.1', # I'll explain this in a second
  keywords = ['testing', 'logging', 'example'], # arbitrary keywords
  classifiers = [],
)