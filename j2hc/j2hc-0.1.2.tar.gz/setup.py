from setuptools import setup

setup(
    name = 'j2hc',
    packages = ['j2hc'],
    version = '0.1.2',
    description = 'Jinja2 extension that removes whitespace between HTML tags',
    author = 'Dmitry Dolgov',
    author_email = '9erthalion6@gmail.com',
    url = 'https://github.com/erthalion/jinja2-htmlcompress',
    download_url = 'https://github.com/erthalion/jinja2-htmlcompress/tarball/0.1.2',
    keywords = ['jinja2', 'html', 'compress'],
    classifiers = [],
    install_requires=[
        'future==0.15.2',
        'Jinja2==2.8'
    ],
)
