from __future__ import print_function


def main(inputfile, **kwdargs):
    pass


def argparser():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile')
    return parser


if __name__ == '__main__':
    main(**vars(argparser().parse_args()))