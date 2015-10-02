from setuptools import setup

setup(
    # Application name:
    name="TransAT_API",

    # Version number (initial):
    version="0.4.6",

    # Application author details:
    author="Ascomp AG",
    author_email="metrailler@ascomp.ch",

    # Packages
    packages=["transat",
              "transat.apps",
              "transat.apps.pipe",
              "transat.apps.3D_pipe",
              "transat.apps.severe_slug",
              "transat.communicator",
              "transat.database",
              "transat.server",
              "transat.postproc",
              "transat.setup",
              "transat.worker",
              "transat.config",
              "transat.coupling",
              "transat.software",
              "transat.tests"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="http://pypi.python.org/pypi/MyApplication_v010/",

    #
    # license="LICENSE.txt",
    description="API (driver) for TransAT, CFD simulation software",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
       "Babel==1.3",
       "Jinja2==2.7.3",
       "MarkupSafe==0.23",
       "Pygments==2.0.2",      
       "Shapely==1.5.9",
       "Sphinx==1.3.1",
       "alabaster==0.7.3",
       "argcomplete==0.8.8",
       "argparse==1.2.1",
       "click==4.0",
       "colorama==0.3.3",
       "docutils==0.12",
       "ecdsa==0.13",
       "mock==1.0.1",
       "nose==1.3.6",
       "numpy==1.9.2",
       "numpy-stl==1.4.2",
       "paramiko==1.15.2",
       "progressbar==2.3",
       "pycrypto==2.6.1",
       "pyparsing==2.0.3",
       "python-dateutil==2.4.2",
       "python-termstyle==0.1.10",
       "python-utils==1.6.2",
       "pytz==2015.2",
       "rednose==0.4.3",
       "requests==2.7.0",
       "six==1.9.0",
       "snowballstemmer==1.2.0",
       "sphinx-rtd-theme==0.1.7",
       "sympy==0.7.6",
       "tinydb==2.3.2",
       "nose==1.3.7",
       "wsgiref==0.1.2",
       "matplotlib==1.4.3"
    ],
)
