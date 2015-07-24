from bgdata import errors, downloader

__version__ = '0.1.1'
__author__ = 'Jordi Deu-Pons'
__author_email__ = 'jordi@jordeu.net'


DEVELOP = downloader.DEVELOP
LATEST = downloader.LATEST

DatasetError = errors.DatasetError
Downloader = downloader.Downloader