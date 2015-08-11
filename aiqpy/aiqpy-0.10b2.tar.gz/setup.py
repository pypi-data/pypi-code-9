import re
from setuptools import setup

with open('aiqpy/__init__.py') as init_file:
    matches = re.finditer(r'__([a-z]*)__\s=\s+\'(.*)\'', init_file.read())
    locals().update({match.group(1): match.group(2) for match in matches})

setup(
    name=title,
    version=version,
    description='Python bindings for connecting to a AIQ8 server',
    author=author,
    author_email=email,
    packages=['aiqpy', 'tools'],
    install_requires=[
        'requests',
        'six',
        'click'
    ],
    keywords=['aiq8', 'appear', 'rest', 'api'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
           'aiqpyprofile = tools.aiqpyprofile:main'
        ]
    }
)
