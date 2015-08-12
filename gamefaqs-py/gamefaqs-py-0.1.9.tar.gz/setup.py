from distutils.core import setup
 
LONG_DESCRIPTION = open('README.rst').read()

setup(
    name='gamefaqs-py',
    version='0.1.9',
    author='Ryan Tonini',
    author_email ='ryantonini@yahoo.com',
    packages=['gamefaqs', 'scripts'],
    url='https://github.com/ryantonini/gamefaqs-py',
    license=' GNU General Public License v3.0',
    description='Retrieve and manage game data from GameFAQS.',
    long_description=LONG_DESCRIPTION,
    package_data={'gamefaqs': ['data/*.sql']},
    scripts=['scripts/load.py']

    #entry_points = {
       # 'console_scripts': [
          #  'load_script = scripts.load:load_script']
    #}
)
