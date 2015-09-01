import logging

from os.path import expanduser, join as path_join, isfile
from subprocess import call

CACHE_PATH = expanduser("~/.godb")
call("mkdir -p {}".format(CACHE_PATH), shell=True)
OBO_PATH = path_join(CACHE_PATH, "go.obo")

import urllib

def _download_obo_if_not_exists():

    if not isfile(OBO_PATH):
        logging.info("Downloading Gene Ontology file to " + OBO_PATH)
        urllib.urlretrieve ("http://geneontology.org/ontology/go.obo",
                            OBO_PATH)
        logging.info("Download finished")

    return OBO_PATH
