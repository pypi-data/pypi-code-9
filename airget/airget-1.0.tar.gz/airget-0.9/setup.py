
from setuptools import setup
import os

os.system('pip install click')
os.system('pip install wget')
os.system('pip install emoji')

setup(name="airget",
	version="0.9",
	description="A simple python package manager.",
	url="https://github.com/Airget/airget-pip",
	author="Aaron Gill-Braun",
	author_email="aarongillbraun@gmail.com",
	license='Apache 2.0',
	packages=["airget"],
	scripts=["bin/airget"],
	zip_safe=False)
