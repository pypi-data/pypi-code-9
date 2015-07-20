#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from setuptools import setup, find_packages
from docs import getVersion


# Variables ===================================================================
changelog = open('CHANGES.rst').read()
long_description = "\n\n".join([
    open('README.rst').read(),
    changelog
])


# Actual setup definition =====================================================
setup(
    name='edeposit.amqp',
    version=getVersion(changelog),
    description="E-Deposit's AMQP definitions and common classes/patterns.",
    long_description=long_description,
    url='https://github.com/edeposit/edeposit.amqp/',

    author='Edeposit team',
    author_email='edeposit@email.cz',

    classifiers=[
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    license='GPL2+',

    packages=find_packages(exclude=['ez_setup']),

    scripts=[
        "bin/edeposit_amqp_tool.py",
        "bin/edeposit_amqp_alephdaemon.py",
        "bin/edeposit_amqp_calibredaemon.py",
        "bin/edeposit_amqp_ftp_monitord.py",
        "bin/edeposit_amqp_ftp_managerd.py",
        "bin/edeposit_amqp_antivirusd.py",
        "bin/edeposit_amqp_harvester.py",
        "bin/edeposit_amqp_ltpd.py",
        "bin/edeposit_amqp_pdfgend.py",
        "bin/edeposit_amqp_downloaderd.py",
        "bin/edeposit_amqp_storaged.py",
    ],

    namespace_packages=['edeposit'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        "python-daemon==1.6",
        "pika>=0.9.13",
        "sh",                # required by edeposit.amqp.ftp for monitor daemon
    ],
    extras_require={
        "test": [
            "pytest",
            "sh"
        ],
        "docs": [
            "sphinx",
            "sphinxcontrib-napoleon",
        ]
    }
)
