#!/usr/bin/python3
#-*- coding:utf-8 -*-

from setuptools import setup
import Kappa.info as info

long_desc = """
Access Twitch.tv from the Shell
Check streams, see viewers, load streams into Livestreamer
"""

conf = {
        "name":"Twitch.py",
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
        "keywords":"twitch livestreamer videogames video games twitch.tv",
        "packages":["Kappa"],
        "install_requires":["Livestreamer", "requests"],
        "extras_require":{},
        "package_data":{},
        "entry_points":{
            "console_scripts":[
                "twitch=Kappa.appa:main"
                ]
            }
        }
setup(**conf)
# end
