try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'logging and convenience functions for phidgets',
    'author': 'Nathan Harrington',
    'url': 'https://github.com/nharringtonwasatch/Phidgeter',
    'download_url': 'https://github.com/nharringtonwasatch/Phidgeter',
    'author_email': 'nharrington@wasatchphotonics.com',
    'version': '1.0.1',
    'install_requires': ['nose', 'testfixtures', 'phidgets'],
    'packages': ['phidgeter'],
    'scripts': [],
    'name': 'Phidgeter'
}

setup(**config)
