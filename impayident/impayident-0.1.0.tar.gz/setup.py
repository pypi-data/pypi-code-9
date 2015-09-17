from __future__ import with_statement

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version():
    with open('impayident/version.txt') as f:
        return f.read().strip()


def get_readme():
    try:
        with open('README.rst') as f:
            return f.read().strip()
    except IOError:
        return ''


setup(
    name='impayident',
    version=get_version(),
    description='Impay Identification tool.',
    long_description=get_readme(),
    author='Jeong YunWon',
    author_email='jeong+impayident@youknowone.org',
    url='https://github.com/bpc/impayident',
    packages=(
        'impayident',
    ),
    package_data={
        'impayident': ['version.txt']
    },
    install_requires=[
        'six', 'requests', 'prettyexc',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
