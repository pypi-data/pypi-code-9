from setuptools import *

kwargs = {
	"author" : "Joe Ellis",
	"author_email" : "joechrisellis@gmail.com",
	"description" : "A deterministic password generator.",
	"entry_points" : {"console_scripts" : ["dtpwgen=deterministicpwgen.frontend:main"]},
	"license" : "GPL v2",
	"name" : "deterministicpwgen",
	"packages" : ["deterministicpwgen"],
	"version" : "V1.1",
}

setup(**kwargs)
