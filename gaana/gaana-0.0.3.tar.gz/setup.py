"""Gaana setup script."""

from setuptools import setup

setup(
    name='gaana',
    version='0.0.3',
    packages=['gaana'],

    # dependencies
    install_requires=[
        'beautifulsoup4==4.3.2',
        'requests==2.5.1',
        'terminaltables==1.1.1',
        'wsgiref==0.1.2'
    ],

    # metadata for upload to PyPI
    author='Love Sharma',
    author_email='contact@lovesharma.com',
    description='Download songs from gaana.com from command line `gaana`',
    keywords='download gaana gana song songs'.split(),
    url='https://github.com/zonito/gaana',  # project homepage
    download_url='https://github.com/zonito/gaana/archive/0.0.3.tar.gz',

    entry_points={
        'console_scripts': [
            'gaana=gaana.gaana:main'
        ]
    }
)
