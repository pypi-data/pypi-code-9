from setuptools import setup, find_packages
import os, sys
import platform

DESCRIPTION = "A Django email backend for Mailgun"

LONG_DESCRIPTION = None
try:
    LONG_DESCRIPTION = open('README.rst').read()
except:
    pass

version = "0.3.0"

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    sys.exit()

if sys.argv[-1] == 'tag':
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Framework :: Django',
]

setup(
    name='django-mailgun-redux',
    version=version,
    packages=['django_mailgun'],
    author='Bradley Whittington, Daniel Roy Greenfeld',
    author_email='pydanny@gmail.com',
    url='http://github.com/pydanny/django-mailgun/',
    license='MIT',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    platforms=['any'],
    install_requires=['requests'],
    classifiers=CLASSIFIERS,
    #TODO: get mailgun into pypi so it can be a requirement :)
)
