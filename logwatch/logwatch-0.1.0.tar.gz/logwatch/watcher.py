#!/usr/bin/env python
import os
import sys
import re
import time
from yamlcfg import YamlConfig
from tail import tail
from mailer import Mailer

SLEEP_DEFAULT = 5.0
config = YamlConfig(name='watcher')

def watch(path, regex, sleep=SLEEP_DEFAULT, verbose=0, empty=False,
        mailer=None):
    while True:
        last_line = tail(path=path, ct=1)
        if last_line is None:
            if empty:
                if verbose:
                    print('File is empty, ignoring.')
                time.sleep(sleep)
                continue
            mailer.send_email('empty log file', '{} is empty.'.format(path))
            time.sleep(sleep)
            continue
        last_line = last_line[0]
        match = regex.match(last_line)
        if match is None:
            mailer.send_email('mismatched log tail',
                'Line did not match:\n{}'.format(last_line))
        elif verbose:
            if match.groupdict():
                print('Groups: {}'.format(
                    ', '.join(
                        [
                            '='.join((x, y))
                            for x, y in match.groupdict().items()
                        ]
                    )
                ))
            elif match.groups():
                print('Groups: {}'.format(', '.join(match.groups())))
            else:
                print('Line matched.')
        time.sleep(sleep)

def main():
    import argparse
    parser = argparse.ArgumentParser(prog='watcher')
    parser.add_argument('path', help='path to log file to watch')
    parser.add_argument('--regex', '-r', 
        help='regex that should pass on last line (default defined in config '
        'file, with $path: {regex: $regex})')
    parser.add_argument('--sleep', '-S', type=float,
        help='time to sleep in between checks (default defined in config '
        'under $path: {{sleep: $sleep}}, or {})'.format(SLEEP_DEFAULT))
    parser.add_argument('--verbose', '-v', action='count',
        help='print regex groups')
    parser.add_argument('--empty-ok', '-e', action='store_true',
        help='will not alert if file is empty')
    args = parser.parse_args()
    path_config = getattr(config, args.path, {})
    regex_str = args.regex or path_config.get('regex')
    sleep = args.sleep or path_config.get('sleep', SLEEP_DEFAULT)
    if regex_str is None:
        sys.exit('No regex supplied, either through command line or config\n')
    regex = re.compile(regex_str)
    mailer_kwargs = config._data
    mailer_kwargs.update(path_config)
    mailer = Mailer(**mailer_kwargs)
    watch(args.path, regex, sleep=sleep, verbose=args.verbose,
        empty=args.empty_ok, mailer=mailer)

if __name__ == '__main__':
    main()
