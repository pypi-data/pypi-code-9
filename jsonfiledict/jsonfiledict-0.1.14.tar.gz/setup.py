from setuptools import setup, find_packages

__version__ = "unknown"

import pyver
__version__, __version_info__ = pyver.get_version (
    pkg = "jsonfiledict",
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
    license = "LGPL v3",
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
