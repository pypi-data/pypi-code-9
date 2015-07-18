# -*- coding: utf-8 -*-

from setuptools import setup

setup(
	name="openweathermapy",
	version="0.6.6",
	url="https://github.com/crazycapivara/openweathermapy",
	download_url="https://github.com/crazycapivara/openweathermapy/archive/master.zip",
	author="Stefan Kuethe",
	author_email="crazycapivara@gmail.com",
	license="GPLv3",
	classifiers=[
		"Development Status :: 3 - Alpha",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Programming Language :: Python",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3.2",
		"Programming Language :: Python :: 3.3",
		"Programming Language :: Python :: 3.4",
		"Topic :: Utilities" 
	],
	keywords="openweathermap, weather data, forecast data, free weather, open weather, API 2.5",
	description="Python package wrapping OpenWeatherMap.org's API 2.5",
	packages = ["openweathermapy"]
)
