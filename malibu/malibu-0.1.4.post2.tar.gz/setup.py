try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

from pip.download import PipSession
from pip.req import parse_requirements
import malibu

install_reqs = parse_requirements("requirements.txt", session = PipSession())
reqs = [str(r.req) for r in install_reqs]

setup(
    name = 'malibu',
    version = malibu.__version__,
    description = "maiome library of utilities",

    url = "http://phabricator.maio.me/tag/malibu",
    author = "Sean Johnson",
    author_email = "sean.johnson@maio.me",

    license = "Unlicense",

    classifiers = [
        "Development Status :: 3 - Alpha",
        "License :: Public Domain",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    packages = ['malibu',
                'malibu.config',
                'malibu.connection',
                'malibu.database',
                'malibu.design',
                'malibu.text',
                'malibu.util'],
    package_dir = {'malibu': 'malibu'},
    install_requires = reqs,
    zip_safe = True
)
