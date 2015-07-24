import argparse
from http.client import HTTPConnection
import logging
import os
from urllib.parse import urlparse
import bgdata


def check_url(url):
    p = urlparse(url)
    conn = HTTPConnection(p.netloc)
    conn.request('HEAD', p.path)
    resp = conn.getresponse()
    return resp.status < 400


def remote_repository_url():
    return os.environ.get("BGDATA_REMOTE", "http://bg.upf.edu/bgdata")


def local_repository_url():

    # Check environment variable
    repository = os.path.expanduser(os.environ.get("BGDATA_LOCAL", "~/.bgdata"))

    # Create the local repository
    if not os.path.exists(repository):
        os.makedirs(repository)

    return repository


def cmdline():

    # Parse the arguments
    parser = argparse.ArgumentParser()

    # Mandatory
    parser.add_argument('project', help='Project name')
    parser.add_argument('dataset', help='Dataset name')
    parser.add_argument('version', help='Dataset version')
    parser.add_argument('-b', '--build', default=bgdata.LATEST, help='Dataset build (default latest)')
    parser.add_argument('-v', '--verbose', dest='verbose', default=False, action='store_true', help="Give more information")
    parser.add_argument('-r', '--remote', dest='remote_repo', default=remote_repository_url(), help="Remote repository URL")
    parser.add_argument('-l', '--local', dest='local_repo', default=local_repository_url(), help="Local repository folder")
    parser.add_argument('-n', '--num-connections', type=int, dest='num_connections', default=4, help="Specify maximum number of connections (default 4)")
    args = parser.parse_args()

    # Configure the logging
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG if args.verbose else logging.INFO)
    logging.debug(args)

    # Create a downloader
    downloader = bgdata.Downloader(
        local_repository=args.local_repo,
        remote_repository=args.remote_repo,
        num_connections=args.num_connections
    )

    # Download the dataset
    dataset_path = downloader.get_path(args.project, args.dataset, args.version, build=args.build)

    logging.info("Dataset downloaded")
    print(dataset_path)

if __name__ == "__main__":
    cmdline()

