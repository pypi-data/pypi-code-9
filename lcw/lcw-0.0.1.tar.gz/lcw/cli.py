import argparse, sys, os

from more_itertools import ilen

from . import lcw

argparser = argparse.ArgumentParser('lcw',
    formatter_class = argparse.ArgumentDefaultsHelpFormatter,
    description = 'Estimate how many lines are in a file.')
argparser.add_argument('file', type = argparse.FileType('rb'))
argparser.add_argument('--sample-size', '-n', type = int, default = 1000, dest = 'n',
                       help = 'How many pages to count')
argparser.add_argument('--page-size', '-p', type = int, default = 2 ** 14,
                       help = 'Size of an observation')
argparser.add_argument('--just-ml', '-j', action = 'store_true',
                       help = 'Only print the maximum likelihood estimate')

def main():
    args = argparser.parse_args()
    if args.n < 1:
        sys.stderr.write('Sample size must be at least one.\n')
        return 1


    if os.stat(args.file.name).st_size > 1.5 * args.page_size:
        stats = lcw.count(args.file, n = args.n, page_size = args.page_size)
        template = '%(ml)d ± %(radius)d lines (99%% confidence)\n'
    else:
        template = '%(ml)d lines (100%% confidence)\n'
        stats = {
            'ml': args.file.read().count(b'\n')
        }

    if args.just_ml:
        sys.stdout.write('%d\n' % stats['ml'])
    else:
        sys.stdout.write(template % stats)

if __name__ == '__main__':
    main()
