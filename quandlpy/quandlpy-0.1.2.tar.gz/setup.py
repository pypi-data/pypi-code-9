from setuptools import setup


setup(
    name='quandlpy',
    packages = ['quandlpy'],
    description='simple Quandl python wrapper',
    version = '0.1.2',
    author = 'Alex Takata',
    author_email = 'takata.alex@gmail.com',
    url = 'https://github.com/ack8006/quandl-py',
    license = 'MIT',
    keywords = 'Quandl Python Wrapper',
    install_requires = [
        'pandas >= 0.14',
        'requests',
    ]
)
