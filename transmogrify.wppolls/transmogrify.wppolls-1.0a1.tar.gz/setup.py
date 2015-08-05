# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = '1.0a1'
description = 'Transmogrifier pipeline sections to import WordPress polls into Plone.'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(
    name='transmogrify.wppolls',
    version=version,
    description=description,
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='import wordpress blog plone transmogrifier pipeline blueprint wxr',
    author='Héctor Velarde',
    author_email='hecto.velarde@gmail.com',
    url='https://github.com/collective/transmogrify.wppolls',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['transmogrify'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'collective.polls',
        'collective.transmogrifier',
        'plone.app.transmogrifier',
        'Products.GenericSetup',
        'setuptools',
        'zope.component',
        'zope.interface',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            'plone.testing',
        ],
    },
    entry_points="""
    # -*- entry_points -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
