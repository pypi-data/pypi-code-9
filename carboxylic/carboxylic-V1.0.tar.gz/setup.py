from setuptools import *

kwargs = {
	"author" : "Joe Ellis",
	"author_email" : "joechrisellis@gmail.com",
	"description" : "A simple, mnemonic based, assembly-esque mini language.",
	"entry_points" : {"console_scripts" : ["carboxylic=carboxylic.carboxylic:main"]},
	"license" : "GPL v2",
	"name" : "carboxylic",
	"packages" : ["carboxylic"],
	"version" : "V1.0",
}

setup(**kwargs)
