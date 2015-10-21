#!/usr/bin/env python -u
from setuptools import setup, find_packages

try:
    import pypandoc

    description = pypandoc.convert('README.md', 'rst') + '\n'
    pypandoc.convert('README.md', 'rst', outputfile='README.rst')
except (IOError, ImportError):
    description = open('README.rst').read()

setup(
    name='stuff-proxy',
    version=".".join(map(str, __import__("stuffproxy").__version__)),
    long_description=description,
    author='Alexandr I. Shurigin',
    author_email='alexandr.shurigin@gmail.com',
    maintainer='Alexandr I. Shurigin',
    maintainer_email='alexandr.shurigin@gmail.com',
    url='https://github.com/phpdude/stuff-proxy',
    license='GPL',
    packages=find_packages(),
    package_data={'stuffproxy': ['templates/*']},
    test_suite='tests',
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
    ],
    entry_points={
        'console_scripts': ['stuff-proxy = stuffproxy.cli:cli']
    },
    install_requires=[
        'click', 'urwid', 'yamlsettings', 'flask', 'uwsgi'
    ]
)
