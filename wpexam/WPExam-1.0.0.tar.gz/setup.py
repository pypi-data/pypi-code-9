try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'creation of pre-populated exam locations',
    'author': 'Nathan Harrington',
    'url': 'https://github.com/nharringtonwasatch/WPExam',
    'download_url': 'https://github.com/nharringtonwasatch/WPExam',
    'author_email': 'nharrington@wasatchphotonics.com',
    'version': '1.0.0',
    'install_requires': [],
    'packages': ['wpexam'],
    'scripts': [],
    'name': 'WPExam'
}

setup(**config)
