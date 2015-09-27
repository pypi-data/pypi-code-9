from setuptools import setup
from widediaper.version.version import __version__

setup(
    name = "widediaper",
    packages = ["widediaper", "widediaper/parse", "widediaper/version", "widediaper/r_session", "widediaper/utils"],
    version = __version__,
    description = "Simple, stable, easily debuggable R/Python piping",
    author = "Endre Bakken Stovner",
    author_email = "endrebak@stud.ntnu.no",
    url = "http://github.com/endrebak/widediaper",
    keywords = ["R", "Statistics"],
    license = ["GPL-3.0"],
    install_requires = ["pandas", "pexpect", "ebs>=0.0.4"],
    classifiers = [
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Topic :: Software Development :: Libraries :: Python Modules"],
    long_description = ("Python/R pipe."
                        "See the url for more info.")
)
