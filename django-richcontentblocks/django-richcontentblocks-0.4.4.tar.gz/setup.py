import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-richcontentblocks',
    version='0.4.4',
    packages=['richcontentblocks'],
    include_package_data=True,
    license='MIT License', 
    description='Simple (rich) content blocks for use on front end templates. With admin tool.',
    long_description=README,
    author='Django Radonich-Camp',
    author_email='django@emergeinteractive.com',
    url = 'https://github.com/django-emerge/django-richcontentblocks',
    download_url = 'https://github.com/django-emerge/django-richcontentblocks/tarball/0.4.4',
    install_requires=[
        'django-ckeditor>=4.5.1'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)