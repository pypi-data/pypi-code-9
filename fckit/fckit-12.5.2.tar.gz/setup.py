# REF: https://packaging.python.org

import setuptools

setuptools.setup(
	name = "fckit", # https://www.python.org/dev/peps/pep-0426/#name
	version = "12.5.2", # https://www.python.org/dev/peps/pep-0440/
	#packages = [], # https://pythonhosted.org/setuptools/setuptools.html#using-find-packages
	description = "Collection of prototyping functions and classes",
	#long_description = "",
	url = "https://github.com/fclaerho/fckit",
	author = "florent claerhout",
	author_email = "code@fclaerhout.fr",
	license = "MIT",
	#classifiers = [], # https://pypi.python.org/pypi?%3Aaction=list_classifiers
	#keyword = [],
	py_modules = ["fckit"],
	#install_requires = [], # https://packaging.python.org/en/latest/requirements.html#install-requires-vs-requirements-files
	#package_data = {},
	#data_files = {},
	#entry_points = {}, # https://pythonhosted.org/setuptools/setuptools.html#automatic-script-creation
	test_suite = "test",
	#tests_require = [],
	#extra_require = {},
	#setup_requires = [],
	#dependency_links = [], # https://pythonhosted.org/setuptools/setuptools.html#dependencies-that-aren-t-in-pypi
)
