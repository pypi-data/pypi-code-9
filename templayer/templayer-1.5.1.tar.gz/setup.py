
from distutils.core import setup

import templayer

version = templayer.__version__

setup (
	name = "templayer",
	version = version,
	description = "Templayer - Layered Template Library for HTML",
	author = "Ian Ward",
	author_email = "ian@excess.org",
	url = "http://excess.org/templayer/",
	license = "LGPL",
	py_modules = ['templayer'],
	)


