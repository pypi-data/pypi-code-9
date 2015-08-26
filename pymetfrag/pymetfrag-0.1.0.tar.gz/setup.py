

######################################################################################
#
# YOU CAN / SHOULD EDIT THE FOLLOWING SETTING
#
######################################################################################

PKG_NAME = 'pymetfrag'

VERSION = (0, 1, 0)

### install package as emzed extension ? #############################################
#   -> package will appear in emzed.ext namespace after installation

IS_EXTENSION = True


### install package as emzed app ?  ##################################################
#   -> can be started as app.hires()
#   set this variable to None if this is a pure extension and not an emzed app

APP_MAIN = None

### author information ###############################################################

AUTHOR = 'Uwe Schmitt'
AUTHOR_EMAIL = 'uwe.schmitt@id.ethz.ch'
AUTHOR_URL = "http://sis.id.ethz.ch"

### package descriptions #############################################################

DESCRIPTION = "Python wrapper of metfrag for ms/ms based identification of LCMS data"

LONG_DESCRIPTION = """

This libraries wraps Metfrag_. It needs pandas installed and works nicley with emzed, though
emhed is not mandatory.

MetFrag_ is a freely available software for the annotaion of high precision
tandem mass spectra of metabolites which is a first and critical step for the
identification of a molecule's structure. Candidate molecules of different
databases are fragmented in silico and matched against mass to charge values. A
score calculated using the fragment peak matches gives hints to the quality of
the candidate spectrum assignment.

.. _Metfrag: http://c-ruttkies.github.io/MetFrag/
"""

INSTALL_REQUIRES = ["pandas"]


LICENSE = "http://opensource.org/licenses/LGPL-2.1"


if APP_MAIN is not None:
    try:
        mod_name, fun_name = APP_MAIN.split(":")
        exec "import %s as _mod" % mod_name
        fun = getattr(_mod, fun_name)
    except:
        raise Exception("invalid specification %r of APP_MAIN" % APP_MAIN)

VERSION_STRING = "%s.%s.%s" % VERSION

ENTRY_POINTS = dict()
ENTRY_POINTS['emzed_package'] = ["package = " + PKG_NAME, ]
if IS_EXTENSION:
    ENTRY_POINTS['emzed_package'].append("extension = " + PKG_NAME)
if APP_MAIN is not None:
    ENTRY_POINTS['emzed_package'].append("main = %s" % APP_MAIN)


if __name__ == "__main__":   # allows import setup.py for version checking

    from setuptools import setup
    setup(name=PKG_NAME,
          packages=[PKG_NAME],
          author=AUTHOR,
          author_email=AUTHOR_EMAIL,
          url=AUTHOR_URL,
          description=DESCRIPTION,
          long_description=LONG_DESCRIPTION,
          license=LICENSE,
          version=VERSION_STRING,
          entry_points=ENTRY_POINTS,
          install_requires=INSTALL_REQUIRES,
          package_data={"pymetfrag": ["pymetfrag/*.jar",
                                      "pymetfrag/*.exe",
                                      "pymetfrag/*.ini",
                                      "pymetfrag/*.txt",
                                      ]
                        }
          )
