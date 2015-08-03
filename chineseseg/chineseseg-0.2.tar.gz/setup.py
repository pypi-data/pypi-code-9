from distutils.core import setup
setup(
  name = 'chineseseg',
  packages = ['chineseseg'], 
  version = '0.2',
  description = 'A Python3 wrapper for a collection of Chinese word segmenter',
  author = 'WenLi Zhuang',
  author_email = 'r03922101@ntu.edu.tw',
  url = 'https://github.com/iamalbert/chinese-segmenter', 
  download_url = 'https://github.com/iamalbert/chinese-second/tarball/0.1', 
  keywords = ['nlp','chinese', 'word', 'segment', 'text'],
  license = 'MIT',
  install_requires=[
    'JPype1',
  ],
  classifiers = [
    "Programming Language :: Python :: 3",
    "Natural Language :: Chinese (Simplified)",
    "Natural Language :: Chinese (Traditional)"
  ],
  package_data = {
    'chineseseg': ['*.class']
  }
)
