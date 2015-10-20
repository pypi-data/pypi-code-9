import logging

from os.path import expanduser, join as path_join, isfile
from subprocess import call

CACHE_PATH = expanduser("~/.godb")
call("mkdir -p {}".format(CACHE_PATH), shell=True)
OBO_PATH = path_join(CACHE_PATH, "go.obo")

try:
    from urllib import urlretrieve
except ImportError:
    from urllib.request import urlretrieve


def _download_obo_if_not_exists():

    if not isfile(OBO_PATH):
        logging.info("Downloading Gene Ontology file to " + OBO_PATH)
        urlretrieve("http://geneontology.org/ontology/go.obo",
                            OBO_PATH)
        logging.info("Download finished")

    return OBO_PATH
