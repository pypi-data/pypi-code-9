from setuptools import setup, find_packages
from codecs import open

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()
with open('CHANGELOG.rst', 'r', 'utf-8') as f:
    changelog = f.read()

setup(
    name='pscore',
    packages=find_packages(),  # this must be the same as the name above
    version='0.2.1.3',
    long_description=readme + '\n\n' + changelog,
    description='Python-Selenium framework module',
    author='Andrew Fowler',
    author_email='andrew.fowler@skyscanner.net',
    package_data={'': ['CHANGELOG.rst']},
    include_package_data=True,
    url='http://example.com',  # use the URL to the github repo
    download_url='https://pypi.python.org/pypi/pscore',  # I'll explain this in a second
    keywords=['selenium', 'webdriver', 'saucelabs', 'grid'],  # arbitrary keywords
    classifiers=[], requires=['selenium'], install_requires=['selenium==2.45.0', 'requests==2.5.1']
)