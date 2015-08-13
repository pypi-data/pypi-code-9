import argparse
parser = argparse.ArgumentParser()
subs = parser.add_subparsers(dest='cmd')

parser1 = subs.add_parser('foo')
parser1.add_argument('--days', '-d', type=int)

parser2 = subs.add_parser('bar')
parser2.add_argument('--nodays', '-n', type=int)

args = parser.parse_args()

print(hasattr(args, 'days'))
