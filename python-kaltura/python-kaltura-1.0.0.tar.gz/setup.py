from distutils.core import setup
from setuptools import find_packages

setup(
    name='python-kaltura',
    version='1.0.0',
    #url='http://www.kaltura.com/api_v3/testme/client-libs.php',
    packages=['KalturaClient', 'KalturaClient.Plugins'],
    #packages=find_packages(),
    license='AGPL',
    description='A Python module for accessing the Kaltura API.',
    long_description=open('README.txt').read(),
    install_requires = [
            'poster',
        ],
    #author='Patrick Tchankue',
    maintainer ='Patrick Tchankue',
    maintainer_email = 'ptchankue@gmail.com',
    keywords = ['kaltura', 'python', 'django', 'flask'], # arbitrary keywords
    url = 'https://github.com/ptchankue/KalturaGeneratedAPIClientsPython',
    download_url = 'https://github.com/ptchankue/KalturaGeneratedAPIClientsPython/tarball/0.1',
)
