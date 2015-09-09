from setuptools import setup

setup(
    name = 'pyokapi',
    version = '0.0.2',
    packages = ['pyokapi',],
    author = 'okapi',
    install_requires = [ 'werkzeug', 'requests', 'easydict'],
    package_data = { 'pyokapi': ['okapi.thrift']},
    author_email = 'okapi@okapi.pub',
    url = 'http://www.okapi.pub/help/python',
    license = 'http://www.okapi.pub/about.html',
    description = 'RESTful API platform okapi python library'
    ) 
