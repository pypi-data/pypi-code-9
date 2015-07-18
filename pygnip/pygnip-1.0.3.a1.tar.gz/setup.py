"""
Python-Gnip
"""
from setuptools import setup


setup(
    name='pygnip',
    version='1.0.3.a1',
    keywords=['gnip api powertrack'],
    url='https://github.com/benjiao/python-gnip',
    license='BSD',
    author='Benjie Jiao',
    author_email='benjiao12@gmail.com',
    description='A wrapper for the Gnip API',
    long_description=__doc__,
    packages=['pygnip'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    test_suite='tests',
    install_requires=[],
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
