from os import path
import playlistingscraper
from setuptools import setup, find_packages


def read(file_path):
    with open(path.join(path.dirname(__file__), file_path)) as f:
        return f.read()


requires = [
    'lxml>=3.4.4',
    'requests>=2.7.0'
]

setup(
    name='playlistingscraper',
    packages=find_packages(exclude=['tests*']),
    install_requires=requires,
    version=playlistingscraper.__version__,
    description='A command line tool that scrpaes the listing details of an app in the Google Play Store and saves it in a JSON file.',
    long_description=read('README.md'),
    author='Khalid Alharbi',
    author_email='kalharbi@users.noreply.github.com',
    url='https://github.com/sikuli/sieveable-tools/tree/master/Play-Listing-Scraper',
    keywords=['google', 'play', 'scraper', 'listing', 'details', 'apps'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Information Analysis'
    ],
    entry_points={
        'console_scripts':
            [
                'playlistingscraper = playlistingscraper.playlistingscraper:playlistingscraper_command'
            ]
    }
)
