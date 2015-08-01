# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :
#
# Paper
# Copyright 2015 ActivKonnect

import os
import codecs
from distutils.core import setup
from pip.req import parse_requirements
from pip.download import PipSession


with codecs.open(os.path.join(os.path.dirname(__file__), 'README.rst'), 'r') as readme:
    README = readme.read()

requirements = parse_requirements(
    os.path.join(os.path.dirname(__file__), 'requirements.txt'),
    session=PipSession()
)

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='paper',
    version='0.1.0',
    packages=['paper'],
    package_dir={'': 'src'},
    include_package_data=True,
    license='WTFPL',
    description='Keep generated fields in cache for your Django models.',
    long_description=README,
    url='https://github.com/ActivKonnect/paper',
    author='Rémy Sanchez',
    author_email='remy.sanchez@activkonnect.com',
    install_requires=[str(x.req) for x in requirements],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Framework :: Django',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Development Status :: 3 - Alpha',
    ]
)
