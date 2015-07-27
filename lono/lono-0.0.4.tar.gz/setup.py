from setuptools import setup
setup(
    name = 'lono',
    packages = ['lono'], # this must be the same as the name above
    version = '0.0.4',
    description = 'A python package to interface with the Lono Public API',
    author = 'Ryan Gaus',
    author_email = 'ryang@lono.io',
    url = 'http://make.lono.io',
    download_url = 'https://github.com/peterldowns/mypackage/tarball/0.1',
    keywords = ['lono', 'sprinkler', 'iot', 'outdoor', 'rachio', 'skydrop', 'water'],
    classifiers = [],
    install_requires=['requests']
)
