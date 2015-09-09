# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='stacks-contentgroup',
    packages=find_packages(),
    version='0.1.2',
    author=u'Jonathan Ellenberger',
    author_email='jonathan_ellenberger@wgbh.org',
    url='http://stacks.wgbhdigital.org/',
    license='MIT License, see LICENSE',
    description=(
        "A Stacks apps for creating groups of menu-ed content."
    ),
    long_description=open('README.md').read(),
    zip_safe=False,
    install_requires=[
        'django-versatileimagefield>=1.0.2',
        'django-textplusstuff>=0.4',
        'stacks-page>=0.1.1'
    ],
    package_data={
        'stacks_contentgroup': [
            'static/sass/*.scss',
            'static/js/*.js',
            'templates/stacks_contentgroup/contentgroup/*.html'
        ]
    },
    classifiers=[
        'Framework :: Django',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Development Status :: 3 - Alpha'
    ]
)
