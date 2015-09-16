#!/usr/bin/python3
#-*- coding:utf-8 -*-

from setuptools import setup
import Diretide.info as info

long_desc = """
Check Dota 2 Tournament Matches from the command line
Uses the Daily Dota 2 Match API
"""

conf = {
        "name":"DotaCLI",
        "version":info.__version__,
        "description":info.__description__,
        "long_description":long_desc,
        "url":info.__url__,
        "author":info.__author__,
        "author_email":info.__email__,
        "license":info.__license__,
        "classifiers":[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.2",
            "Programming Language :: Python :: 3.3",
            "Programming Language :: Python :: 3.4",
            ],
        "keywords":"dota2 dota 2 livestreamer twitch games cli",
        "packages":["Diretide"],
        "install_requires":["requests"],
        "extras_require":{},
        "package_data":{},
        "entry_points":{
            "console_scripts":[
                "dota-matches=Diretide.app:main"
                ]
            }
        }
setup(**conf)
# end
