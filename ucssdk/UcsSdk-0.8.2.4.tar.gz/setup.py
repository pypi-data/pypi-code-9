#!/usr/bin/python

import sys
import os
from setuptools import setup
from setuptools.command.install import install as _install
from setuptools.command.easy_install import chmod, current_umask
from distutils import log

if sys.version_info < (2, 4) or sys.version_info[0] == 3:
    raise DistutilsError("This package requires Python 2.4 or higher versions 2.x not Python3")

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),r"src/UcsSdk"))
from Version import __version__

name='UcsSdk'
files = ["UcsConfig.cfg", "resources/SyncMoConfig.xml"]
in_place_scripts = ["UcsHandle.py", "UcsHandle_Edit.py", "WatchUcsGui.py", "UcsHandle.py", "CcoImage.py", "ConvertFromBackup.py"]

def is_package(path):
	return (
			os.path.isdir(path) and
			os.path.isfile(os.path.join(path, '__init__.py'))
			)

def find_packages(path, base="" ):
	packages = {}
	for item in os.listdir(path):
		dir = os.path.join(path, item)
		if is_package( dir ):
			if base:
				module_name = "%(base)s.%(item)s" % vars()
			else:
				module_name = item
			packages[module_name] = dir
			packages.update(find_packages(dir, module_name))
	return packages

class install(_install):
	def run(self):
		_install.run(self)
		# set the execute bit on scripts that are NOT copied to a bin dir
		for in_place_script in in_place_scripts:
			if os.name == 'posix' and not self.dry_run:
				target = os.path.join(self.install_lib, name, in_place_script)
				log.info("Set execute bit on: "+ target)
				chmod(target, 0o777 - current_umask())
				
setup(
	name=name,
	version=__version__,
	description='Python SDK for Cisco UCS Manager',
	author='Cisco Systems',
	author_email='',
	long_description='Install Instructions: sudo python setup.py install',
	license='LICENSE.txt',
	cmdclass={'install': install},
	packages=find_packages('src'),
	package_dir = {'': 'src'},
	include_package_data = True,
	zip_safe = False,
	)
