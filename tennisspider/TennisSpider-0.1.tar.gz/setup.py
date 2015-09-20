from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name = "TennisSpider",
    version = "0.1",
    packages = ['TennisSpider'],
    author = "Dmitry Dubov",
    author_email = "dmitry.s.dubov@gmail.com",
    description = "Package for parsing info about tennis results and stats.",
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    license = "PSF",
    keywords = "Tennis, Results",
    url = "https://github.com/cs-hse-projects/DataSpider_Dubov", 
    entry_points={
        'console_scripts':
            ['get_tennis=TennisSpider.main:main']
        }
)