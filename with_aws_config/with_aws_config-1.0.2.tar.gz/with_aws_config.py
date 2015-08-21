#!/usr/bin/env python -B

'''
with_aws_config loads profile information stored by 'aws configure', sets
the environment variables expected by the AWS CLI, EC2 CLI, Ansible, and
'boto', runs the specified command, and exits with its status code.

AWS_DEFAULT_REGION and EC2_URL will default to 'us-west-2' if not configured
during 'aws configure'.

Examples, all running 'ec2-describe-instances' with the default profile:

    with_aws_config -- ec2-describe-instances
    with_aws_config -p default -- ec2-describe-instances
    env AWS_DEFAULT_PROFILE=default with_aws_config -- ec2-describe-instances

Environment variables:

    AWS_PROFILE           used to specify profile if --profile not given
    AWS_DEFAULT_PROFILE   used if AWS_PROFILE not given
    HOME                  required to locate $HOME/.aws

Environment variable modifications before running COMMAND:

    AWS_ACCESS_KEY        specified for EC2 CLI
    AWS_ACCESS_KEY_ID     specified for AWS CLI, boto
    AWS_CONFIG_FILE       stripped (ignored if supplied)
    AWS_DEFAULT_PROFILE   stripped (used as above if supplied)
    AWS_DEFAULT_REGION    specified for AWS CLI
    AWS_PROFILE           stripped (used as above if supplied)
    AWS_SECRET_ACCESS_KEY specified for AWS CLI, boto
    AWS_SECRET_KEY        specified for EC2 CLI
    AWS_SESSION_TOKEN     stripped (ignored if supplied)
    EC2_URL               specified for EC2 CLI

Files:

   $HOME/.aws/config
   $HOME/.aws/credentials
'''


from __future__ import print_function

import argparse
import ConfigParser
import os
import os.path
import subprocess
import sys

__all__ = [
    'main',
    'determine_profile',
    'load_aws_config',
    'run_command_with_aws_config',
    'store_aws_config_to_environment',
]

STRIP = [
    'AWS_ACCESS_KEY',
    'AWS_ACCESS_KEY_ID',
    'AWS_CONFIG_FILE',
    'AWS_DEFAULT_PROFILE',
    'AWS_DEFAULT_REGION',
    'AWS_PROFILE',
    'AWS_SECRET_ACCESS_KEY',
    'AWS_SECRET_KEY',
    'AWS_SESSION_TOKEN',
    'EC2_URL',
]

EXIT_NO_CONFIG = 124
EXIT_NO_SECTION = 125
EXIT_NOT_FOUND = 127   # convention
EXIT_SIGINT = 128 + 2  # convention


def main():
    'Run _main, catching ^C.'
    try:
        _main()
    except KeyboardInterrupt:
        gripe('Interrupted by user.')
        sys.exit(EXIT_SIGINT)


def _main():
    'Tie it all together.'

    args = parse_cli_args()
    command = [args.command] + args.args

    exit_if_no_config(os.environ, exit)

    profile, source = determine_profile(os.environ, args.profile)
    verbose = gripe if args.verbose else noop

    verbose('# loading AWS profile %s specified by %s...' % (repr(profile), source))

    try:
        aws_config = load_aws_config(os.environ, profile)

    except ConfigParser.NoSectionError, err:
        gripe("Can't find config section: %s." % repr(err.section))
        if source == 'default':
            gripe("Do you need to set --profile or AWS_PROFILE?")
        else:
            gripe("Please check ~/.aws against %s." % source)
        sys.exit(EXIT_NO_SECTION)

    try:
        status = run_command_with_aws_config(aws_config, command, verbose)
        sys.exit(status)

    except OSError, err:
        if err.errno == 2:
            gripe('%s: command not found' % command[0])
        else:
            gripe('%s' % err)
        sys.exit(EXIT_NOT_FOUND)


def exit_if_no_config(environ, _exit=sys.exit):
    'exit(EXIT_NO_CONFIG) if we can not find the configuration files.'

    home = environ.get('HOME', '')
    config = os.path.join(home, '.aws', 'config')
    credentials = os.path.join(home, '.aws', 'credentials')

    if len(home) == 0:
        gripe("HOME not set; can't load configuration")

    elif not os.path.isfile(config):
        gripe("%s: no such file" % config)

    elif not os.path.isfile(credentials):
        gripe("%s: no such file" % credentials)

    else:
        return # phew!

    _exit(EXIT_NO_CONFIG)


def parse_cli_args():
    'Parse the command line arguments.'

    parser = argparse.ArgumentParser(
        description="Set AWS envars from 'aws configure', then run a command.",
        epilog=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('command', metavar='COMMAND', type=str,
                        help='command to run')
    parser.add_argument('args', metavar='ARGUMENT', type=str, nargs='*',
                        help='command arguments')
    parser.add_argument('--verbose', '-v', action='store_true', default=False,
                        help='output debugging information to stderr')
    parser.add_argument('--profile', '-p', action='store', default=None,
                        help='set the profile, ignoring AWS_DEFAULT_PROFILE')

    return parser.parse_args()


def noop(*args):
    'do nothing'
    return args


def run_command_with_aws_config(aws_config, command, verbose=noop):
    'Run a command with environment variables derived from `aws_config`.'

    env = strip_keys(os.environ, STRIP)
    store_aws_config_to_environment(aws_config, env, verbose)
    verbose('# running command:\n%s\n# output:' % ' '.join(command))
    status = subprocess.call(command, env=env)
    verbose('# exit status: %d' % status)
    return status


def strip_keys(source, keys):
    'Strip keys in `keys` from the source dict `source`. Destructive.'

    return dict((k, v) for (k, v) in source.iteritems() if k not in keys)


def determine_profile(environ, profile=None):
    'Determine the AWS profile to use.'

    if profile is not None:
        return profile, 'your --profile argument'

    elif environ.has_key('AWS_PROFILE'):
        return environ['AWS_PROFILE'], 'AWS_PROFILE'

    elif environ.has_key('AWS_DEFAULT_PROFILE'):
        return environ['AWS_DEFAULT_PROFILE'], 'AWS_DEFAULT_PROFILE'

    else:
        return 'default', 'default'


def load_aws_config(environ, profile):
    'Load AWS config details from the files `aws configure` maintains.'

    home = environ['HOME']
    aws_config = load_raw_config(os.path.join(home, '.aws', 'config'), region='us-west-2')
    aws_credentials = load_raw_config(os.path.join(home, '.aws', 'credentials'))

    return dict(
        region=aws_config.get('profile %s' % profile, 'region'),
        aws_access_key_id=aws_credentials.get(profile, 'aws_access_key_id'),
        aws_secret_access_key=aws_credentials.get(profile, 'aws_secret_access_key')
    )


def load_raw_config(path, **defaults):
    'Load an inifile-style configuration file from `path` with `defaults`.'

    config = ConfigParser.RawConfigParser(defaults)
    config.read(path)
    return config


def store_aws_config_to_environment(config, target, verbose=noop):
    'Store AWS config details to the `target` environment dict'

    updates = dict(
        EC2_URL='https://ec2.%s.amazonaws.com' % config['region'],
        AWS_DEFAULT_REGION=config['region'],
        AWS_ACCESS_KEY=config['aws_access_key_id'],
        AWS_SECRET_KEY=config['aws_secret_access_key'],
        AWS_ACCESS_KEY_ID=config['aws_access_key_id'],
        AWS_SECRET_ACCESS_KEY=config['aws_secret_access_key'],
    )

    for (key, value) in updates.iteritems():
        verbose('export %s=%s' % (key, value))
        target[key] = value


def gripe(message):
    'Gripe to standard error.'

    print(message, file=sys.stderr)


if __name__ == '__main__':
    main()
