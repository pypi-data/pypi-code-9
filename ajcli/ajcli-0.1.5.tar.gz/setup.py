
import os, pip, sys

# from pip.req import parse_requirements

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# if not sys.version_info[0] == 3:
#     print("Sorry, Python 2 is not supported (yet)")
#     sys.exit(1) # return non-zero value for failure

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

install_reqs = pip.req.parse_requirements('requirements.txt', session=pip.download.PipSession())

requirements = [str(ir.req) for ir in install_reqs if ir is not None]

setup(name             = "ajcli",
      author           = "Aljosha Friemann",
      author_email     = "aljosha.friemann@gmail.com",
      #license          = "Beerware",
      version          = "0.1.5",
      description      = "another jira interface including cli",
      url              = "https://bitbucket.org/afriemann/jiracli",
      keywords         = ['cli', 'jira', 'development'],
      # download_url     = "",
      install_requires = requirements,
      long_description = read('README.rst'),
      classifiers      = [],
      packages         = ["jira"],
      entry_points     = {'console_scripts': ['jiracli=jira.cli:run']}
)
