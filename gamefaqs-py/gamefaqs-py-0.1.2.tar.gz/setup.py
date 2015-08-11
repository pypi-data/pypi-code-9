from distutils.core import setup
 
LONG_DESCRIPTION = open('README.rst').read()

setup(
    name='gamefaqs-py',
    version='0.1.2',
    author='Ryan Tonini',
    author_email ='ryantonini@yahoo.com',
    packages=['gamefaqs'],
    url='https://github.com/ryantonini/gamefaqs-py',
    license='GPLv3',
    description='Retrieve and manage game data from GameFAQS.',
    long_description=LONG_DESCRIPTION,
    package_data={'gamefaqs': ['data/dump.sql']},
    scripts=['gamefaqs/scripts/load_data.py']
)
