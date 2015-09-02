import os, logging
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

logger = logging.getLogger("boxup_weatherradar setup")

filename = "boxup_weatherradar/boxup_weatherradar.cfg"

try:
	import shutil

	# copy cfg file
	logger.info("copy cfg to /etc/boxup/plugins/boxup_weatherradar.cfg")
	shutil.copyfile(filename, "/etc/boxup/plugins/boxup_weatherradar.cfg")
	logger.info("done")

except IOError:
	logger.error("Cannot copy boxup_weatherradar.cfg to /etc/boxup/boxup_weatherradar.cfg")

v = "0.0.1"

setup(
    name = "boxup_weatherradar",
    version = v,
    author = "Maximilian, Noppel",
    author_email = "noppelmax@googlemail.com",
    description = ("datasource for boxup input"),
    license = "GPLv2, see LICENSE.txt",
    keywords = ["weatherradar", "openweathermap", "raspberrypi", "gpio", "adafruit", "bicolormatrix"],
    url = "https://github.com/xamgreen/boxup_weatherradar",
		download_url = "https://github.com/xamgreen/boxup_weatherradar/tarball/"+v,
    packages=['boxup_weatherradar'],
    long_description=read('README.md'),
		install_requires = ["boxup_core==0.0.1", "RPi.GPIO>=0.5.11"]
)
