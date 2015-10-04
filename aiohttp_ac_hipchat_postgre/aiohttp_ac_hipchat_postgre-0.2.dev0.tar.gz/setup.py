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
    name='aiohttp_ac_hipchat_postgre',
    packages=find_packages(exclude=["tests*"]),
    version='0.2.dev0',
    url='https://bitbucket.org/ramiroberrelleza/aiohttp-ac-hipchat-postgre',
    license='APLv2',
    author='Ramiro Berrelleza',
    author_email='rberrelleza@atlassian.com',
    description='Postgre store for aiohttp_ac_hipchat',
    long_description=read('README.rst'),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
          'PyJWT==1.4.0',
          'SQLAlchemy==1.0.8',
          'aiohttp==0.17.2'
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
