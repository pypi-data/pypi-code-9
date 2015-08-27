"""
Created on Mar 17, 2015

@author: Jason Bowles
"""
from setuptools import setup
import re, os, io


def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(name="raw_data_emca",
      install_requires = ["sqlalchemy","pandasql","pandas"],
      version=find_version("rawdata_emca/runner/__init__.py"),
      description="application to help data analyst, Extract, Manipulate, Clean, and Analyze their data",
      author="Jason Bowles",
      author_email='jaykbowles@gmail.com',
      url = "https://github.com/jkbowle/RawDataProcessing",
      platforms=["any"],  # or more specific, e.g. "win32", "cygwin", "osx"
       # Choose your license
      license='MIT',

      # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
      ],
      packages = ['rawdata_emca','rawdata_emca.connections', 'rawdata_emca.errors', 'rawdata_emca.processor','rawdata_emca.runner','rawdata_emca.utilities'],
      entry_points = {
        "console_scripts": ['rawdata_cli = rawdata_emca.runner.raw_data_cli:main']
        }
      )