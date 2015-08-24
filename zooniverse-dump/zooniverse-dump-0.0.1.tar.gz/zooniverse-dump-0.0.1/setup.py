try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
}

setup(
    name = 'zooniverse-dump',
    description = 'Panoptes Export Reader/Converter',
    version = '0.0.1',
    author = 'Zooniverse',
    author_email = 'dev@zooniverse.org',
    url = 'https://github.com/zooniverse/panoptes-export-reader',
    entry_points = {
        'console_scripts': ['panoptes-expand=panoptes.cli:expand']
    },
    install_requires=[
        'pandas'
    ]
)
