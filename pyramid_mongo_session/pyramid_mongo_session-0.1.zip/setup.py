"""
You can try https://pypi.python.org/pypi/mongodb-beaker2 which released in 2012... I couldn't, I gave up.


# encoding: utf-8

from pyramid.config import Configurator
from pyramid_mongo_session import MongoSessionFactory
...

def main(global_config, **settings):
    config = Configurator(settings=settings)

    session_factory = MongoSessionFactory(
        collection=MongoClient('localhost', 27017).your_db.session)
    config.set_session_factory(session_factory)
    ...
    return config.make_wsgi_app()

Documentation: https://github.com/tark-hidden/pyramid_mongo_session
"""
from setuptools import setup

setup(
    name='pyramid_mongo_session',
    version='0.1',
    url='https://github.com/tark-hidden/pyramid_mongo_session',
    license='BSD',
    author='Tark',
    maintainer="Tark",
    author_email='tark.hidden@gmail.com',
    description='MongoDB-based session factory for Pyramid framework',
    keywords="pyramid mongodb mongo session factory",
    long_description=__doc__,
    py_modules=['pyramid_mongo_session'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Pyramid',
        'pymongo'
    ],
    test_suite="tests",
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]    
)
