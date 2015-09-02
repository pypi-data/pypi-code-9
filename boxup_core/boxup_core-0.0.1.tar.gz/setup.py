import os, logging
from pkg_resources import Requirement, resource_filename
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

logger = logging.getLogger("boxup-core setup")

filename = "boxup-core/boxup-core.cfg"

try:
	import shutil

	# create cfg-directory
	logger.info("creating cfg-folder at /etc/boxup...")
	if not os.path.exists("/etc/boxup/"):
		os.mkdir("/etc/boxup")
		logger.info("done")
	logger.info("path already exists. nothing to do.")
	
	# create plugin cfg-directory
	logger.info("creating plugin cfg-folder at /etc/boxup/plugins")
	if not os.path.exists("/etc/boxup/plugins/"):
		os.mkdir("/etc/boxup/plugins")
		logger.info("done")
	logger.info("path already exists. nothing to do.")

	# copy cfg file
	logger.info("copy cfg to /etc/boxup/boxup_core.cfg")
	shutil.copyfile("boxup_core/boxup_core.cfg", "/etc/boxup/boxup_core.cfg")

except IOError:
	logger.error("Cannot copy boxup-core.cfg to /etc/boxup/boxup-core.cfg")

try:
	# copy boxup to init.d
	logger.info("copy boxup to /etc/init.d/boxup")
	shutil.copyfile("boxup", "/etc/init.d/boxup")	
	os.system("update-rc.d boxup defaults")
except IOError:
	logger.error("Cannot copy boxup to /etc/init.d/boxup")


v = "0.0.1"

setup(
    name = "boxup_core",
    version = v,
    author = "Maximilian, Noppel",
    author_email = "noppelmax@googlemail.com",
    description = ("The main boxup programm for showing different datasources at different visualizations"),
    license = "GPLv2, see LICENSE.txt",
    keywords = ["weatherradar", "openweathermap", "raspberrypi", "gpio", "diy"],
    url = "https://github.com/xamgreen/boxup_core",
		download_url = "https://github.com/xamgreen/boxup_core/tarball/"+v,
    packages=['boxup_core','boxup_types'],
    long_description=read('README.md')
)
