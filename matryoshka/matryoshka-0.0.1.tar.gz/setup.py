from setuptools import setup, find_packages

setup(
    name = 'matryoshka',
    version = '0.0.1',
    keywords = ('matryoshka', 'icon'),
    description = 'To cut small images from a original image in batch, just like the Matryoshka Dolls.',
    license = 'MIT License',
    install_requires = ['PIL'],

    author = 'JackyShen',
    author_email = 'mebusw@gmail.com',
    
    packages = find_packages(),
    platforms = 'any',
)