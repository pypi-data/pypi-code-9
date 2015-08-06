try:
	from setuptools import setup
except ImportError:
	from disutils.core import setup

config = {
		'description' : 'Colorizes tones in Hanzi and Pinyin from ChinesePod vocab list export in a format that Anki can import',
		'author' : 'Alex Keyes',
		'author_email' : 'alexander.r.keyes@gmail.com',
		'version': '0.7',
		'install_requires' : ['nose', 'zhon', ],
		'packages' : ['cp_to_anki_colorizer'],
		'scripts' : ['bin/cp_to_anki_colorizer'],
		'name' : 'cp_to_anki_colorizer'
}

setup(**config)
