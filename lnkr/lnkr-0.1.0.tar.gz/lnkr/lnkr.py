import os
import sys
import argparse
import glob
import plistlib
import datetime
import pytz
from blessings import Terminal

from app_config import AppConfig
from package_config import PackageConfig
from wrapper_config import WrapperConfig
import processor

PACKAGE_CONFIG_FILE_NAME = 'lnkr-export.toml'
WRAPPER_CONFIG_FILE_NAME = 'lnkr-wrapper.toml'
APP_CONFIG_FILE_NAME = 'lnkr-import.toml'

EXIT_CODE_NO_CONFIG = 1
EXIT_CODE_DISALLOW_PACKAGE_CONFIG = 2
EXIT_CODE_DISALLOW_APP_CONFIG = 3
EXIT_CODE_INVALID_SECTION = 4


ALL = 'all'
YES = 'yes'
NO = 'no'

term = Terminal()

pwd = os.path.abspath('.')

test_mode = False
verbose_mode = False

skip_change_confirm = False

def info(msg):
    print term.normal + msg

def verbose(msg):
    if verbose_mode:
        info(msg)

def error(msg):
    print term.red + msg

def format_error(err):
    return term.red(err)

def format_path(path):
    return term.blue(path)

def format_param(param):
    return term.yellow(param)

def get_section_value(kind, values, key, optional):
    if not isinstance(values, dict):
        error('[%s] Section Should Be Dict: %s' % (kind, values))
    if values.has_key(key):
        return values[key]
    elif optional:
        return None
    else:
        error('[%s] Invalid Section: %s Not Exist -> %s' % (kind, key, values))
        sys.exit(EXIT_CODE_INVALID_SECTION)

def get_attribs(attribs_holders):
    attribs = {}
    for holder in attribs_holders:
        if not hasattr(holder, 'attribs'):
            continue
        for key in holder.attribs:
            value = holder.attribs[key]
            if attribs.has_key(key):
                old_value = attribs[key]
                if old_value != value:
                    info('Attrib Overrided: %s, %s -> %s' % (key, value, old_value))
            else:
                attribs[key] = value
    return attribs

def query_all_yes_no(question, default=None):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"all": ALL, "a": ALL,
             "yes": YES, "y": YES,
             "no": NO, "n": NO}
    if default is None:
        prompt = " [a/y/n] "
    elif default == ALL:
        prompt = " [A/y/n] "
    elif default == YES:
        prompt = " [a/Y/n] "
    elif default == NO:
        prompt = " [a/y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        error('\n' + question + format_param(prompt))
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            error("Please respond with 'all' or 'yes' or 'no' "
                             "(or 'a' or 'y' or 'n').\n")

def confirm_change(question, default=None):
    global skip_change_confirm
    if skip_change_confirm:
        return True
    answer = query_all_yes_no(question, default)
    if answer == ALL:
        skip_change_confirm = True
        return True
    elif answer == YES:
        return True
    return False

def load_app_config(path):
    config = AppConfig(os.path.join(path, APP_CONFIG_FILE_NAME))
    if config.valid:
        return config
    else:
        return None

def load_package_config(path):
    config = PackageConfig(os.path.join(path, PACKAGE_CONFIG_FILE_NAME))
    if config.valid:
        return config
    else:
        return None

def load_wrapper_config(path):
    config = WrapperConfig(os.path.join(path, WRAPPER_CONFIG_FILE_NAME))
    if config.valid:
        return config
    else:
        return None

def load_config(allow_package, allow_app):
    config = load_package_config(pwd) or load_app_config(pwd)
    if config is None:
        error('Lnkr Config File Not Found: %s' % format_path(pwd))
        sys.exit(EXIT_CODE_NO_CONFIG)
    elif isinstance(config, PackageConfig):
        if allow_package:
            verbose('Packeg Config Loaded: %s' % format_path(config.path))
            return config
        else:
            sys.exit(EXIT_CODE_DISALLOW_PACKAGE_CONFIG)
    elif isinstance(config, AppConfig):
        if allow_app:
            verbose('App Config Loaded: %s' % format_path(config.path))
            return config
        else:
            sys.exit(EXIT_CODE_DISALLOW_APP_CONFIG)
    else:
        return None

def do_lint_package(package_config):
    info('Under Construction!')

def do_lint_app(app_config):
    info('Under Construction!')

def do_lint(args):
    config = load_config(True, True)
    if isinstance(config, PackageConfig):
        do_lint_package(config)
    elif isinstance(config, AppConfig):
        do_lint_app(config)

def do_clean(args):
    app_config = load_config(False, True)
    info('Under Construction!')

def do_diff(args):
    app_config = load_config(False, True)
    info('Under Construction!')

def do_link(args):
    app_config = load_config(False, True)
    processor.do_link_app(app_config)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-t', '--test', action='store_true',
                        help='Test Only, Do not do any real change')

    parser.add_argument('-l', '--lint', action='store_true',
                        help='Validate the lnkr config files')
    parser.add_argument('-c', '--clean', action='store_true',
                        help='Clean all links created by lnkr')
    parser.add_argument('-d', '--diff', action='store_true',
                        help='Show diffs between original files vs local files')

    args = parser.parse_args()
    global verbose_mode
    verbose_mode = args.verbose
    global test_mode
    test_mode = args.test

    global skip_change_confirm
    skip_change_confirm = False

    if args.lint:
        do_lint(args)
    elif args.clean:
        do_clean(args)
    elif args.diff:
        do_diff(args)
    else:
        do_link(args)
