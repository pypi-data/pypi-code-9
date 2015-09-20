from setuptools import setup

setup(
    name = 'pyokapi',
    version = '0.0.3.2',
    packages = ['pyokapi',],
    author = 'okapi',
    install_requires = [ 'werkzeug', 'requests-oauthlib', 'easydict'],
    author_email = 'okapi@okapi.pub',
    url = 'http://www.okapi.pub/help/python',
    license = 'http://www.okapi.pub/about.html',
    description = 'RESTful API platform okapi python library'
    ) 
