# -*- coding: utf-8 -
#
# This file is part of django-pwutils released under the MIT license. 
# See the LICENSE for more information.

import os
from setuptools import setup, find_packages

tests_require = [
    'django-webtest>=1.5.7,<2.0',
    'webtest>=2.0.6,<3.0',

    'django-whatever']

jenkins_require = tests_require[:]

if os.environ.get('DJANGO_VERSION') == '1.5':
    jenkins_require += [
        'django-jenkins==0.15.0',
        'django-discover-runner==1.0',
        ]
else:
    jenkins_require += [
        'django-jenkins==0.16.4',
        ]

jenkins_require += [
    'pyflakes==0.7.3',
    'flake8==2.4.1',
    'pylint==1.4.4',
    'pep8==1.4.6',
    'coverage==3.7.1',

    'django-coverage',
]


setup(
    name='django-pwutils',
    version=__import__('pwutils').VERSION,
    description='Django specific utils and helpers',
    long_description=open('README.md').read(),
    author='Suvit Org',
    author_email='mail@suvit.ru',
    license='MIT',
    url='http://bitbucket.org/suvitorg/django-pwutils',
    zip_safe=False,
    packages=find_packages(exclude=['docs', 'examples', 'tests']),
    install_requires=[#'django<1.4',
                      'lockfile'],
    extras_require = {
        'celery': ["django-celery>=2.3.3"],
        'storages': ['pytils'],
        'thumbs': ["Pillow",
                   "sorl-thumbnail"],
        'sphinxsearch': ['elementflow',
                         'django-sphinx'],
        'tests': tests_require,
        'jenkins': jenkins_require,
        'admintools': ['django-admin-tools>=0.5.1,<0.6',
                       'FeedParser'],
        'devel': ['django-debug-toolbar',
                 ],
    },
    tests_require=tests_require,
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Environment :: Web Environment',
        'Topic :: Software Development',
    ]
)
