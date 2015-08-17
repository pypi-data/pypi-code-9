# necessary to push to PyPI
# cf. http://peterdowns.com/posts/first-time-with-pypi.html
# cf. https://tom-christie.github.io/articles/pypi/


from setuptools import setup, find_packages

with open('README.rst') as f:
    long_description = f.read()

setup(
  name = 'ezprettyjson',
  packages = ['ezprettyjson'],
  version = '0.1.1',
  description = 'easy json: dynamic exploration of a dict or json in the notebook',
  long_description = long_description,
  author = 'oscar6echo',
  author_email = 'olivier.borderies@gmail.com',
  url = 'https://github.com/oscar6echo/ezprettyjson', # use the URL to the github repo
  download_url = 'https://github.com/oscar6echo/ezprettyjson/tarball/0.1.1', # tag number at the end
  keywords = ['json', 'dict', 'javascript'], # arbitrary keywords
  license='MIT',
  classifiers = [ 'Development Status :: 4 - Beta',
                  'License :: OSI Approved :: MIT License',
                  'Programming Language :: Python :: 2.7'
  ],
  include_package_data=True,
  package_data={},
)