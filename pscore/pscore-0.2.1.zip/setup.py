from setuptools import setup, find_packages

setup(
    name='pscore',
    packages=find_packages(),  # this must be the same as the name above
    version='0.2.1',
    description='Python-Selenium framework module',
    author='Andrew Fowler',
    author_email='andrew.fowler@skyscanner.net',
    url='http://example.com',  # use the URL to the github repo
    download_url='https://pypi.python.org/pypi/pscore',  # I'll explain this in a second
    keywords=['selenium', 'webdriver', 'saucelabs', 'grid'],  # arbitrary keywords
    classifiers=[], requires=['selenium'], install_requires=['selenium==2.45.0', 'requests==2.5.1']
)