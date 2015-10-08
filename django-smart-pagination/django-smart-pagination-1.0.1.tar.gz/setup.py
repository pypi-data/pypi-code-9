import os
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-smart-pagination',
    version='1.0.1',
    packages=find_packages(exclude=['tests']),
    description='Generate pagination links in Django Templates',
    long_description=long_description,
    url='https://github.com/livioribeiro/django-smart-pagination',
    author='Livio Ribeiro',
    author_email='livioribeiro@outlook.com',
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],

    keywords='django pagination page links',
    install_requires=['Django'],
    extras_require={
        'test': ['pytest', 'pytest-cov', 'pytest-django', 'Jinja2'],
    }
)
