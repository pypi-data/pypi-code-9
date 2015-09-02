import os, logging
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

logger = logging.getLogger("boxup_gmailunread setup")

filename = "boxup_gmailunread/boxup_gmailunread.cfg"

try:
	import shutil

	# copy cfg file
	logger.info("copy cfg to /etc/boxup/plugins/boxup_gmailunread.cfg")
	shutil.copyfile(filename, "/etc/boxup/plugins/boxup_gmailunread.cfg")
	logger.info("done")

except IOError:
	logger.error("Cannot copy gmailunread.cfg to /etc/boxup/gmailunread.cfg")

v = "0.0.2"

setup(
    name = "boxup_gmailunread",
    version = v,
    author = "Maximilian, Noppel",
    author_email = "noppelmax@googlemail.com",
    description = ("datasource of unread emails for boxup input."),
    license = "GPLv2, see LICENSE.txt",
    keywords = ["gmail", "raspberrypi", "gpio"],
    url = "https://github.com/xamgreen/boxup_gmailunread",
		download_url = "https://github.com/xamgreen/boxup_weatherradar/tarball/"+v,
    packages=['boxup_gmailunread'],
		install_requires = ["boxup_core>=0.0.2"]
)
