# -*- coding: UTF-8 -*-
import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

install_requirements = [
	"Django>=1.8",
	"argparse>=1.2.1",
	"requests>=2.6.0",
	"simplejson>=3.6.5",
	"jsonfield>=1.0.3",
	"wsgiref>=0.1.2"
]

setup(
    name='django-gerencianet',
    version='0.1.4',
    packages=['gerencianet'],
    include_package_data=True,
    license='BSD License',  # example license
    description='Uma aplicação django para comunicar com o gateway de pagamento Gerencianet',
    long_description=README,
    url='https://github.com/sidneycarlos65/django-gerencianet',
    author='Sidney Machado',
    author_email='sidney.machado@starlinetecnologia.com.br',
    install_requires=install_requirements,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
    ],
)
