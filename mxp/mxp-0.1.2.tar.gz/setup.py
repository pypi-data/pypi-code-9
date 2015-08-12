from distutils.core import setup
setup(
    name = "mxp",
    packages = ["mxp"],
    version = "0.1.2",
    description = "qPCR fileformat reader",
    author = "Florian FInkernagel",
    author_email = "finkernagel@imt.uni-marburg.de",
    url = "http://www.imt.uni-marburg.de",
    keywords = ["qPCR", "MXP"],
    install_requires=[
                  'olefile',
                  'pandas',
                        ],

    classifiers = [
        "Programming Language :: Python",
        #"Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    long_description = """\
            Reads raw qPCR data from .mxp files and turns it into pandas dataframes.
"""
)
