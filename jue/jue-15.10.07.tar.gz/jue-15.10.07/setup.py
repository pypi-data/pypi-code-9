from setuptools import setup, find_packages

setup(
    name = 'jue',
    version = '15.10.07',
    keywords = ('jue', 'cloud'),
    description = 'Jue Resource SDK for Python',
    license = 'MIT License',
    install_requires = ['requests'],

    author = 'homeway',
    author_email = 'xiaocao.grasses@gmail.com',
    
    packages = find_packages(),
    platforms = 'any',
)