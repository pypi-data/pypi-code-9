import sys
from setuptools import setup, find_packages

setup(  
    name = "fuzzyworkbench",
    version = "0.1.1",
    description = "Fuzzy GUI editor for fuzzylib",
    packages = find_packages(),
    install_requires = ['fuzzylib'],
	author = 'Leandro Mattioli',
	author_email = 'leandro.mattioli@gmail.com',
	entry_points = {
	 'gui_scripts': ['fuzzyeditor = fuzzyworkbench.fuzzyworkbench:main']
	},
	license='LGPL',
	url='http://www.pythonhosted.org/fuzzyworkbench'
)
