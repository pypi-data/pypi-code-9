#!/usr/bin/env python
import os
import sys
import signal
import re
import time
import lockfile
import daemon
from yamlcfg import YamlConfig
from tail import tail
from mailer import Mailer


SLEEP_DEFAULT = 5.0

def check(path, regex, verbose=0, empty=False, mailer=None):
    last_line = tail(path=path, ct=1)
    # Empty file
    if last_line is None:
        if empty:
            if verbose:
                print('File is empty, ignoring.')
            return
        if mailer:
            mailer.send_email('empty log file', '{} is empty.'.format(path))
        return
    last_line = last_line[0]
    match = regex.match(last_line)
    # Regex failed
    if match is None:
        if verbose:
            print('Mismatched log tail for path {}: {}'.format(path, last_line))
        if mailer:
            mailer.send_email('mismatched log tail',
                'Line did not match:\n{}'.format(last_line))
        return
    # Regex passed, so NOP if not verbose, or just print the groups.
    if verbose:
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

def compile_regexs(configs, regex_str=None):
    if regex_str is not None:
        regex = re.compile(regex_str)
        return {
            path: regex
            for path in configs
        }
    else:
        return {
            path: re.compile(log_conf['regex'])
            for path, log_conf in configs.items()
        }

def load_configs(config_path=None, path=None):
    if config_path is None:
        # Default configuration
        base_config = YamlConfig(name='logwatch')
    else:
        # Use explicit config
        base_config = YamlConfig(path=config_path)
    # If --path was not passed, so all logfiles are to be watched
    if path is None:
        # Unless explicit, paths must exist in config.
        if not base_config.logfiles:
            sys.exit('Configuration file must contain "logfiles" definition, or --path must be passed.\n'
                'See example config for details.')
        paths = base_config['logfiles'].keys()
    else:
        paths = [path]
    # Use default settings first
    log_configs = {
        ipath: base_config._data.copy()
        for ipath in paths
    }
    # If there are logfile specific settings for the path, update that log
    # config with them, and clean up the log configs.
    if base_config.logfiles:
        for path, conf in log_configs.items():
            conf.update(base_config.logfiles.get(path, {}))
            del conf['logfiles']
    return base_config, log_configs

def make_mailer(config):
    # If no_mail is set to True, disable it for this config.
    if config.get('no_mail'):
        return None
    return Mailer(**config)

def loop(base_config, configs, regexs, sleep=None, verbose=0, empty=False):
    # First check if it's passed via the command line,
    # if not, check if it's in the paths/global config,
    # finally, use the default.
    sleep = sleep or base_config.sleep or SLEEP_DEFAULT
    while True:
        for path, conf in configs.items():
            regex = regexs[path]
            # Config may have its own mailto, or from, or be disabled.
            mailer = make_mailer(conf)
            # Use config specific empty if it exists.
            empty0 = empty or conf.get('empty', False)
            # Use the max verbosity of log file or command line.
            verbose0 = max(verbose, conf.get('verbose', 0))
            check(
                path, regex, verbose=verbose0, empty=empty0, mailer=mailer,
            )
        time.sleep(sleep)

def daemon_context(working_dir, pid_path):
    context = daemon.DaemonContext(
        working_directory=working_dir,
        umask=0o002,
        pidfile=lockfile.FileLock(pid_path),
    )
    context.signal_map = {
        signal.SIGHUP: 'terminate',
        signal.SIGTERM: 'terminate',
    }
    return context
