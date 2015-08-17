import argparse, sys, os, re

from . import lcw

argparser = argparse.ArgumentParser('lcw',
    formatter_class = argparse.ArgumentDefaultsHelpFormatter,
    description = 'Estimate how many lines are in a file.')
argparser.add_argument('file', type = argparse.FileType('rb'), nargs = '+')
argparser.add_argument('--sample-size', '-n', type = int, default = 1000, dest = 'n',
                       help = 'How many pages to count')
argparser.add_argument('--page-size', '-p', type = int, default = 2 ** 14,
                       help = 'Size of an observation')
argparser.add_argument('--pattern', '-e', default = b'\n',
                       type = lambda x: x.encode('utf-8'),
                       help = 'The pattern to match')
argparser.add_argument('--regex', '-r', action = 'store_true',
                       help = 'Use regular expressions (statistically unsound)')

def main():
    args = argparser.parse_args()
    if args.n < 1:
        sys.stderr.write('Sample size must be at least one.\n')
        return 1

    max_filename_length = max(len(fp.name) for fp in args.file)
    for fp in args.file:
        if os.stat(fp.name).st_size > args.n * args.page_size:
            try:
                stats = lcw.count(fp, n = args.n, page_size = args.page_size,
                                  pattern = args.pattern, regex = args.regex)
            except ValueError as e:
                sys.stderr.write(str(e) + '\n')
                return 1

            template = '%(fn)s%(space)s%(ml)d ± %(radius)d occurrences (99%% confidence)\n'
        else:
            template = '%(fn)s%(space)s%(ml)d occurrences (100%% confidence)\n'
            if args.regex:
                ml = len(re.findall(args.pattern, fp.read()))
            else:
                ml = fp.read().count(args.pattern)
            stats = {
                'ml': ml,
            }

        stats.update({
            'fn': fp.name,
            'space': (max_filename_length + 1 - len(fp.name)) * ' ',
        })

        sys.stdout.write(template % stats)

if __name__ == '__main__':
    main()
