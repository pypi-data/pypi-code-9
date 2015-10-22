import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.txt')).read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'django-luhublog',
    version = "0.1.11",
    packages = ["luhublog"],
    include_package_data = True,
    license = "BSD License",
    description = "Blog app",
    long_description = README,
    url = "www.luhu.es",
    author = "John Sanchez",
    author_email = "johnsanchezc@luhu.es",
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires = [
        'Django==1.8.5',
        'django-model-utils==2.3.1',
	    'django-bleach==0.3.0',
        'Pillow',
        'sorl-thumbnail==12.3',
        'beautifulsoup4',
        'django-froala-editor',
        'django-taggit',
        'django-classy-tags',
        'django-imagekit',
    ],
)
