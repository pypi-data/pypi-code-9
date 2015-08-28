import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('filename', metavar='filename', type=str, nargs=1,
                   help='Original large image to be cut')
parser.add_argument('-i', '--integers', metavar='N', type=int, nargs='+',
                   help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                   const=sum, default=max,
                   help='sum the integers (default: find the max)')

print parser.parse_args(['-i', '7', '-1', '42', '--sum', '/Users/jacky/work/17sports-mui/images/mdpi.png'])
# print parser.parse_args(['7', '-1', '42'])

args = parser.parse_args()
print args.accumulate(args.integers)
print args.filename
