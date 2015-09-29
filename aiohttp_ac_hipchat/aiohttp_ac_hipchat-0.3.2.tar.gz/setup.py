import codecs
import os
from setuptools import setup, find_packages


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, *parts), 'rb', 'utf-8') as f:
        return f.read()

setup(
    name='aiohttp_ac_hipchat',
    packages=find_packages(exclude=["tests*"]),
    version='0.3.2',
    url='https://bitbucket.org/atlassianlabs/aiohttp_ac_hipchat',
    license='APLv2',
    author='Julien Hoarau',
    author_email='julien@atlassian.com',
    description='Aiohttp extension to support Atlassian Connect for HipChat',
    long_description=read('README.rst'),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'aiohttp',
        'asyncio_mongo',
        'PyJWT',
        'asyncio_redis'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)