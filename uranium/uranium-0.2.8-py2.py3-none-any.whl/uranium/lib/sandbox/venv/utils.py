import logging
import os
import sys
from virtualenv import create_environment

LOGGER = logging.getLogger(__name__)

PREFIX = getattr(sys, "prefix", None)
REAL_PREFIX = getattr(sys, "real_prefix", None)


def install_virtualenv(install_dir):
    if is_virtualenv(install_dir):
        return

    original_prefix = sys.prefix
    if hasattr(sys, "real_prefix"):
        sys.prefix = sys.real_prefix

    create_environment(install_dir, no_setuptools=False,
                       no_pip=True, site_packages=False,
                       symlink=False)

    sys.prefix = original_prefix


VIRTUALENV_FILES = {
    'activate file': os.path.join('bin', 'activate')
}


def is_virtualenv(path):
    """ validate if the path is already a virtualenv """
    for name, venv_path in VIRTUALENV_FILES.items():
        target_path = os.path.join(path, venv_path)
        if not os.path.exists(target_path):
            return False
    return True
