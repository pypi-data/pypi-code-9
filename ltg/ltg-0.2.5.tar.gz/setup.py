
import os, pip

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

package = 'ltg'

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def read_version():
    version = {}
    with open('%s/version.py' % package, 'rb') as init_file:
        exec(init_file.read(), version)

    return version['__version__']

def read_requirements():
    install_reqs = pip.req.parse_requirements('requirements.txt', session=pip.download.PipSession())
    return [str(ir.req) for ir in install_reqs if ir is not None]

setup(name             = package,
      version          = read_version(),
      author           = 'Aljosha Friemann',
      author_email     = 'aljosha.friemann@gmail.com',
      description      = 'link to git',
      license          = None,
      keywords         = ["utility", "configuration", "git", "linux"],
      url              = 'https://bitbucket.org/afriemann/ltg',
      download_url     = 'https://pypi.python.org/pypi/ltg',
      packages         = [package],
      install_requires = read_requirements(),
      long_description = read('README'),
      classifiers      = [],
      entry_points     = {'console_scripts': ['ltg=%s.cli:run' % package]}
)
