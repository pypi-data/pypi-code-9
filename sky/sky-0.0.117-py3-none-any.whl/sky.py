import argparse

from sky.view import view


def get_args_parser():
    p = argparse.ArgumentParser(
        description='sky is the limit.')
    p.add_argument('-view', '-v', action='store_true',
                   help='Use the skyViewer (demo NewsCrawler)')
    return p


def main():
    """ This is the function that is run from commandline with `gittyleaks` """
    args = get_args_parser().parse_args()
    if args.view:
        view.main()
