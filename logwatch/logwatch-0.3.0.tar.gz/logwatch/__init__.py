''' logwatch

Stupid small script to alert when a log is messing up - easier than setting up nagios right now
'''

import sys
import os
import watcher

def setup():
    print('''
Configuration files' authority are in this order, from most important to least:
 * --config command line argument
 * ./.logwatch.{yml,yaml}
 * ~/.logwatch.{yml,yaml}
 * ~/.config/logwatch/config.{yml,yaml}
 * /etc/config/logwatch/config.{yml,yaml}

Variables from a less authoritative config will be used unless overridden
by a higher configuration, such as that passed by --config.

This means that if "sleep: 60" is defined in /etc/config/logwatch/config.yml,
it will be used unless another existing configuration defines "sleep: 30", and
so on.
''')
    FINAL_CONFIG_PATH = os.path.expanduser('~/.config/logwatch/example_config.yml')
    EXAMPLE_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'logwatch', '.example_config.yml')
    if not os.path.exists(FINAL_CONFIG_PATH):
        try:
            import shutil
            os.makedirs(os.path.dirname(FINAL_CONFIG_PATH))
            shutil.copyfile(EXAMPLE_CONFIG_PATH, FINAL_CONFIG_PATH)
            print('Example configuration dropped to {}'.format(FINAL_CONFIG_PATH))
        except Exception:
            print('Please see documentation to see example configuration file.')
    else:
        print('Please see example configuration at {}'.format(FINAL_CONFIG_PATH))

def main():
    import argparse
    parser = argparse.ArgumentParser(prog='watcher')
    parser.add_argument('--path', '-p', help='path to log file to watch')
    parser.add_argument('--daemonize', '-d', action='store_true',
        help='daemonize %(prog)s')
    parser.add_argument('--config', '-c',
        help='path to configuration file (defaults to .logwatch.yml')
    parser.add_argument('--regex', '-r', 
        help='regex that should pass on last line (default defined in config '
        'file, with $path: {regex: $regex})')
    parser.add_argument('--setup', '-s', action='store_true',
        help='deploy example configuration and print notes')
    parser.add_argument('--sleep', '-S', type=float,
        help='time to sleep in between checks (default defined in config '
        'under $path: {{sleep: $sleep}}, or {})'.format(watcher.SLEEP_DEFAULT))
    parser.add_argument('--verbose', '-v', action='count',
        help='print regex groups')
    parser.add_argument('--empty-ok', '-e', action='store_true',
        help='will not alert if file is empty')
    args = parser.parse_args()
    if args.setup:
        setup()
        sys.exit(0)
    base_config, configs = watcher.load_configs(config_path=args.config, path=args.path)
    compiled = watcher.compile_regexs(configs, regex_str=args.regex)
    try:
        if not args.daemonize:
            watcher.loop(
                base_config, configs, compiled, 
                sleep=args.sleep, verbose=args.verbose, empty=args.empty_ok,
            )
        else:
            context = watcher.daemon_context(
                base_config.working_dir or '.',
                base_config.pid_path or '/tmp/logwatch.pid',
            )
            with context:
                watcher.loop(
                    base_config, configs, compiled, 
                    sleep=args.sleep, verbose=args.verbose, empty=args.empty_ok,
                )
            raise NotImplementedError('Daemonization incomplete.')
    except KeyboardInterrupt:
        print('Done.')
    
if __name__ == '__main__':
    main()
