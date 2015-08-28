from setuptools import setup, find_packages

setup(
    name = 'matryoshka',
    version = '0.0.2',
    keywords = ('matryoshka', 'icon'),
    description = 'To cut small images from a original image in batch, just like the Matryoshka Dolls.',
    license = 'MIT License',
    install_requires = ['Pillow'],

    author = 'JackyShen',
    author_email = 'mebusw@gmail.com',
    
    packages = find_packages(),
    platforms = 'any',
)