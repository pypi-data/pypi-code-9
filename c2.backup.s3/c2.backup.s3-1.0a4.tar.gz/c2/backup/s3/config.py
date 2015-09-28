
import os
import logging

LOG_FILE_NAME = "c2backups3.log"
YAML_FIEL_NAME = "c2backups3.yaml"


logging.basicConfig(
    # level=logging.DEBUG,
    level=logging.WARNING,
    filename=LOG_FILE_NAME,
    format="%(asctime)s %(levelname)s %(funcName)s %(message)s")
error = logging.error
info = logging.info


