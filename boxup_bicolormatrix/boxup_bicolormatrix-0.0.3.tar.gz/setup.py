import os, logging
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

logger = logging.getLogger("boxup_bicolormatrix setup")

filename = "boxup_bicolormatrix/boxup_bicolormatrix.cfg"

try:
	import shutil

	# copy cfg file
	logger.info("copy cfg to /etc/boxup/plugins/boxup_bicolormatrix.cfg")
	if not os.path.exists("/etc/boxup/plugins/boxup_bicolormatrix.cfg"):
		shutil.copyfile(filename, "/etc/boxup/plugins/boxup_bicolormatrix.cfg")
		logger.info("done")
	logger.info("path already exists. nothing to do.")

except IOError:
	logger.error("Cannot copy boxup_bicolormatrix.cfg to /etc/boxup/boxup_bicolormatrix.cfg")

v = "0.0.3"

setup(
    name = "boxup_bicolormatrix",
    version = v,
    author = "Maximilian, Noppel",
    author_email = "noppelmax@googlemail.com",
    description = ("a visualization implementation for boxup. uses a adafruit bicolor matrix 8x8"),
    license = "GPLv2, see LICENSE.txt",
    keywords = "weatherradar openweathermap raspberrypi gpio i2c adafruit bicolormatrix",
    url = "https://github.com/xamgreen/boxup_bicolormatrix",
		download_url="https://github.com/xamgreen/boxup_bicolormatrix/tarball"+v,
    packages=['boxup_bicolormatrix'],
		install_requires = ["boxup_core>=0.0.2"]
)
