#! /usr/bin/env python

try:
  import pyver # pylint: disable=W0611
except ImportError:
  import os, subprocess
  try:
    environment = os.environ.copy()
    cmd = "pip install pyver".split (" ")
    subprocess.check_call (cmd, env = environment)
  except subprocess.CalledProcessError:
    import sys
    print >> sys.stderr, "Problem installing 'pyver' dependency."
    print >> sys.stderr, "Please install pyver manually."
    sys.exit (1)
  import pyver # pylint: disable=W0611

from setuptools import setup, find_packages

__version__, __version_info__ = pyver.get_version (pkg = "jsonfiledict",
                                                   public = True)

setup (
    name = "jsonfiledict",
    version = __version__,
    description = "A dict optionally backed by an auto-updating JSON file.",
    long_description = file ("README.rst").read (),
    classifiers = [],
    keywords = "",
    author = "J C Lawrence",
    author_email = "claw@kanga.nu",
    url = "http://kanga.nu/~claw/",
    license = "GPL v3",
    packages = find_packages (exclude = ["tests",]),
    package_data = {
    },
    zip_safe = False,
    install_requires = [line.strip ()
                        for line in file ("requirements.txt").readlines ()],
    entry_points = {
        "console_scripts": [
        ],
    },
)
