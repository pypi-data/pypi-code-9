from setuptools import setup


setup(
    name='mspdiary',
    version='0.0.1',
    description='Daily diary',
    long_description='README.md',
    license='BSD',
    author='Michael Pace',
    author_email='mpace1027@gmail.com',
    url='http://github.com/michaelpace/mspdiary/',
    py_modules=['mspdiary'],
    install_requires=[],
    entry_points={
              'console_scripts': [
                  'mspdiary = mspdiary:main',                  
              ],              
          },
    keywords=['diary']
)
