from setuptools import setup
from os import path

# get __version__
execfile("pong/__init__.py")


setup(
	name = 'pong',
	version = __version__,
	description = 'Fast visualization and analysis of population structure',
	author = 'Aaron A. Behr, Gracie Liu-Fang, Katherine Z. Liu, Priyanka Nakka, and Sohini Ramachandran',
	author_email = 'aaron_behr@alumni.brown.edu',
	url = 'https://bitbucket.org/abehr/pong',
	# download_url = 'https://github.com/abehr/pkg/tarball/0.1',
	keywords = ['population','genetics','clustering'],
	classifiers = [
		"Development Status :: 4 - Beta",
		"Intended Audience :: Science/Research",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Natural Language :: English",
		"Operating System :: MacOS :: MacOS X",
		"Operating System :: POSIX :: Linux",
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 2.7",
		"Topic :: Scientific/Engineering :: Bio-Informatics"],
	provides = ["pong"],
	requires = [
		"numpy (>=1.9.2)",
		"tornado",
		"munkres (>=1.0.7)" # "cairosvg"],
	],
	install_requires = [
		"numpy", "tornado", "munkres" #, "cairosvg"
	],
	# dependency_links=['https://pypi.python.org/pypi'],
	packages = ["pong"],
	# package_data = {"pong": ["static/*", "templates/*"]},
	# scripts=["run_script/pong"]
	# package_data = { "pong": [ 'static/pong.min.css', 'static/pong.min.js', 'templates/pong.html' ] },
	# scripts = [ 'run_script/pong' ]
	package_data = { "pong": ['pong.min.css', 'pong.min.js', 'pong.html'] },
	scripts = [ 'run_script/pong' ]


)