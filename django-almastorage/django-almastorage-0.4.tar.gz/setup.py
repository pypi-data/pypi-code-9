import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-almastorage',
    version='0.4',
    packages=['almastorage'],
    include_package_data=True,
    description='A simple Django app to use SwiftStack Storage',
    long_description=README,
    url='https://github.com/aaannnyyy/django-almastorage',
    author='Nurlan Abyken',
    author_email='abyken.nurlan@gmail.com',
    install_requires=['django>=1.5', 'python-swiftclient', 'django-tastypie', 'requests'],
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
    ],
)
