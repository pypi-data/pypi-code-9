"""
Flask-SES
-------------

Flask extension for interfacing with AWS' SES service.
"""
from setuptools import setup


setup(
    name='Flask-SES',
    author='Stuart Robertson',
    author_email='stooie.robertson@gmail.com',
    version='0.1.1',
    url='https://github.com/stooie90/flask-ses',
    license='MIT',
    description='Flask extension for interfacing with AWS\' SES service',
    long_description=__doc__,
    packages=['flask_ses'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'boto'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
