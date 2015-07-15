import os
from setuptools import setup


try:
    from pypandoc import convert
    README = convert('README.md', 'rst')
except ImportError:
    with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
        README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='airavata',
    version='0.9.3',
    packages=['airavata', 'airavata.management.commands', 'airavata.templatetags'],
    include_package_data=True,
    license='BSD License',
    description='Multiple dynamic sistes with Django',
    long_description=README,
    url='http://bb.levit.be/djang-airavata',
    author='Levit SCS',
    author_email='emma@levit.be',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=['Django>=1.8', 'django-allowedsites']
)
