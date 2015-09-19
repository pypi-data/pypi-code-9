try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Simple Ast Visualization Tool',
    'author': 'Robert Heumueller',
    'url': 'http://github.com/compiler-dept/astviz',
    'download_url': 'https://github.com/compiler-dept/astviz/archive/master.zip',
    'author_email': 'code@heum.de',
    'version': '0.1.1',
    'install_requires': ['grako', 'graphviz'],
    'packages': ['astviz'],
    'package_data': {'astviz': ['Ast.ebnf']},
    'entry_points': {'console_scripts': ['astviz = astviz.astviz:main',]},
    'license': "MIT",
    'name': 'astviz'
}

setup(**config)
