#!/usr/bin/env python
try:
    from setuptools import setup, find_packages
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name = 'flask-media',
    version = '0.4.1',
    description = 'Flask extestion helper uploads files',
    long_description = '\n' + open('README').read(),
    author='Vadim Statishin',
    author_email = 'statishin@gmail.com',
    keywords = 'flask file upload image',
    license = 'BSD License',
    url = 'http://bitbucket.org/cent/flask-media/',
    #tests_require = ['nose', 'webtest'],
    #test_suite='nose.collector',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    platforms='any',
    zip_safe = True,
    packages = find_packages(),
    include_package_data=True,

    requires=['Flask', 'sqlalchemy', 'Pillow'],
    install_requires=['Flask'],
)
