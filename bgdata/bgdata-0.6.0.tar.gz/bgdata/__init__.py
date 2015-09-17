import logging
import os
import sys
from bgdata import errors, downloader

__version__ = '0.6.0'
__author__ = 'Jordi Deu-Pons'
__author_email__ = 'jordi@jordeu.net'

DEVELOP = downloader.DEVELOP
LATEST = downloader.LATEST

DatasetError = errors.DatasetError
Downloader = downloader.Downloader

# Logging config
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


# Default repository locations
def remote_repository_url():
    return os.environ.get("BGDATA_REMOTE", "http://bg.upf.edu/bgdata")


def local_repository_url():

    # Check environment variable
    repository = os.path.expanduser(os.environ.get("BGDATA_LOCAL", "~/.bgdata"))

    # Create the local repository
    if not os.path.exists(repository):
        os.makedirs(repository)

    return repository

# Create a default downloader
downloader = Downloader(
    local_repository=local_repository_url(),
    remote_repository=remote_repository_url(),
    num_connections=4
)

# Shortcut to default methods
get_path = downloader.get_path
is_downloaded = downloader.is_downloaded
