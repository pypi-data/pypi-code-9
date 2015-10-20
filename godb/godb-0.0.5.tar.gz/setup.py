from setuptools import setup

from godb.config.version import __version__

setup(
    name = "godb",
    packages = ["godb", "godb/config", "godb/get_and_parse_data",  "godb/messy_df_to_user_data"],
    version = __version__,
    description = "A set of annotation maps describing most of the Gene Ontology.",
    author = "Endre Bakken Stovner",
    author_email = "endrebak@stud.ntnu.no",
    url = "http://github.com/endrebak/godb",
    keywords = ["Gene Ontology"],
    license = ["GPL-3.0"],
    install_requires = ["pandas>=0.16", "joblib"],
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
        "Topic :: Scientific/Engineering"],
    long_description = ("A set of annotation maps describing most of the Gene Ontology. See the webpage for more info."))
