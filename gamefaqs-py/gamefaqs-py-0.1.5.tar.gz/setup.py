import setuptools
from distutils.core import setup
 
LONG_DESCRIPTION = open('README.rst').read()

setup(
    name='gamefaqs-py',
    version='0.1.5',
    author='Ryan Tonini',
    author_email ='ryantonini@yahoo.com',
    packages=['gamefaqs', 'gamefaqs.scripts'],
    url='https://github.com/ryantonini/gamefaqs-py',
    license='GPLv3',
    description='Retrieve and manage game data from GameFAQS.',
    long_description=LONG_DESCRIPTION,
    #package_data={'gamefaqs': ['data/dump.sql']},
    entry_points = {
        'console_scripts': [
            'load_script = gamefaqs.scripts.load:load_script']
    }
)
