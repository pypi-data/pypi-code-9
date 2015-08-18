#!/usr/bin/python

from setuptools import setup

import sys

opts = dict()
if sys.platform == 'win32':
	import py2exe
	opts.update(
		dict(
			zipfile=None,
			options={
				'py2exe':{
					'includes': ['docopt'],
					'bundle_files': 1
				}
			},
			console=["eagle_automation/pea.py"],
		))
	# windows=[
	#     {
	#         'script': 'eagle_automation/artool.py',
	#         # 'icon_resources': [(1, 'moduleicon.ico')]
	#     }
	# ],

if sys.argv[0] == 'setup.py':
    print("SETUP PY CALLED")
    opts.update(dict(
        long_description_markdown_filename='README.md',
        setup_requires=['setuptools_markdown'],
    ))
else:
    print("SETUP PY NOT CALLED", sys.argv)

setup(
	name='eagle_automation',
	version='0.1.3',
	description='Simple scripts supporting open hardware development using CadSoft EAGLE',
	license='GPL',
	author='Tomaz Solc, Bernard Pratz',
	author_email='tomaz.solc@tablix.org, guyzmo+pea@m0g.net',
	url='',
	packages=['eagle_automation'],
	classifiers=[
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.7',
		'Development Status :: 4 - Beta',
		'License :: OSI Approved',
		'Operating System :: Unix',
	],
	install_requires=[
		'pillow',
		'docopt',
		'setuptools',
	],
	entry_points="""
	# -*- Entry points: -*-
	[console_scripts]
	pea = eagle_automation.pea:main
	""",
    **opts
)

if sys.argv[0] == 'setup.py' and 'install' in sys.argv:
    print("To start using this tool, do `pea --help`")
