
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'pystatuspage is a simple api wrapper for statuspage api',
    'author': 'Eran Zimbler',
    'url': 'https://github.com/srgrn/pystatuspage',
    'author_email': 'eran@zimbler.net',
    'version': '0.0.1',
    'install_requires': ['requests'],
    'packages': ['pystatuspage'],
    'name': 'pystatuspage',
    'keywords': ['api_wrapper', 'statuspage', 'statuspage.io'],  # arbitrary keywords
}

setup(**config)
