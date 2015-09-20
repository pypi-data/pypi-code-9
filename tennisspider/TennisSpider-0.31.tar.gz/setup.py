from setuptools import setup, find_packages

setup(
    name = "TennisSpider",
    version = "0.31",
    packages = ['TennisSpider'],
    author = "Dmitry Dubov",
    author_email = "dmitry.s.dubov@gmail.com",
    description = "Package for parsing info about tennis results and stats.",
    license = "PSF",
    keywords = "Tennis, Results",
    url = "https://github.com/cs-hse-projects/DataSpider_Dubov", 
    entry_points={
        'console_scripts':
            ['get_tennis=TennisSpider.main:main']
        }
)