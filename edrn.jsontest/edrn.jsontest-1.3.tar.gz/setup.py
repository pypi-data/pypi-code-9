import setuptools
#from distutils.core import setup
from setuptools import find_packages, setup

setup(
    name='edrn.jsontest',
    namespace_packages= ['edrn'],
    version='1.3',
    description='A test module',
    url='https://github.jpl.nasa.gov/yuliu/edrn.test.git',
    download_url= 'https://github.jpl.nasa.gov/yuliu/edrn.test/tarball/1.0',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['anyjson','jsonlib2'],
    entry_points = {
        'console_scripts': [
            'jsontest = edrn.jsontest.main:main']
    }
)
