import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("remote_url", help="url of the remote git repository (https or ssh)")
    parser.add_argument("destination", nargs="?", help="directory to clone repository to")
    return parser.parse_args()