from setuptools import *

kwargs = {
    "author" : "Joe Ellis",
    "author_email" : "joechrisellis@gmail.com",
    "description" : "Generates diceware/xkcd style passwords.",
    "entry_points" : {"console_scripts" : ["dicepass=dicepass.dicepass:main"]},
    "license" : "GPL v2",
    "name" : "dicepass",
    "packages" : ["dicepass"],
    "version" : "V1.0",
}

setup(**kwargs)
