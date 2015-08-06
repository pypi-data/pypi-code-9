try:
	from setuptools import setup
except ImportError:
	from disutils.core import setup

config = {
		'description' : 'Colorizes ChinesePod output into Anki-compatible format',
		'author' : 'Alex Keyes',
		'author_email' : 'alexander.r.keyes@gmail.com',
		'version': '0.5',
		'install_requires' : ['nose'],
		'packages' : ['cp_to_anki_colorizer'],
		'scripts' : [],
		'name' : 'cp_to_anki_colorizer'
}

setup(**config)
