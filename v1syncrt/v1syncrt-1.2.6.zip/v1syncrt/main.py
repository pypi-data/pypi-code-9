""""Main script, identifies parameters from sys.argv
    and runs scripts in order they have being called"""
__author__ = 'glucero'

from configobj import ConfigObj
from v1pysdk import V1Meta
import ssl
import sys
import argparse
from add_regression_test import main as main_regression_test
from add_to_suite import main as main_add_to_suite
from sync_tests import main as main_sync_tests
from sync_regression_suites_tags import main as main_sync_rs_tags
from update_results import main as main_update_results
from yarara.runner import run_scenarios
import os


reload(sys)
sys.setdefaultencoding('utf8')


def main(args_list=sys.argv[1:]):
    command_list = ['add_regression', 'add_to_suite', 'sync_tests', 'sync_rs_tags']
    command_mains = {
        'add_regression': main_regression_test,
        'add_to_suite': main_add_to_suite,
        'sync_tests': main_sync_tests,
        'sync_rs_tags': main_sync_rs_tags,
    }

    v1config = ConfigObj('versionone_config.cfg')

    # Check if the username and password is in the parameters
    parser = argparse.ArgumentParser()
    if 'username' in v1config:
        parser.add_argument('-u', '--username', required=False,
                            help='The username of VersionOne Client.',
                            default=v1config['username'])
    else:
        parser.add_argument('-u', '--username', required=True,
                            help='The username of VersionOne Client.')
    if 'password' in v1config:
        parser.add_argument('-p', '--password', required=False,
                            help='The password of VersionOne Client.',
                            default=v1config['password'])
    else:
        parser.add_argument('-p', '--password', required=True,
                            help='The password of VersionOne Client.')

    v1config.setdefault('yarara_base_dir', '../')

    parser.add_argument('--yarara_dir', required=False,
                        help='Base directory of Yarara project',
                        default=v1config['yarara_base_dir'])

    for command in command_list:
        parser.add_argument('--' + command, action='store_true', default=False)
    parser.add_argument('--sync_all', action='store_true', default=False)
    parser.add_argument('--sync_only', action='store_true', default=False)
    parser.add_argument('--update_results', required=False, default=None)

    parser.add_argument('--features', required=False, default=None)

    args, run_scenarios_args = parser.parse_known_args(args_list)
    print run_scenarios_args

    common_args = [sys.argv[0], '-p', args.password, '-u', args.username,
                   '--yarara_dir', args.yarara_dir]

    v1config['username'] = args.username
    v1config['password'] = args.password
    v1config['yarara_base_dir'] = args.yarara_dir

    print '\nVersionOne config: ' + str(v1config)
    for attr in ['instance_url', 'project']:
        assert attr in v1config, ('Missing attribute %s on versionone_config.cfg' % attr)

    if args.sync_all:
        for command in command_list:
            setattr(args, command, True)

    # Open version one sdk
    if v1config.get('verify_certificates', 'true') == 'false':
        ssl._create_default_https_context = ssl._create_unverified_context
    v1m = V1Meta(instance_url=v1config['instance_url'],
                 username=v1config['username'], password=v1config['password'])

    os.chdir(os.path.join(v1config['yarara_base_dir'], 'project'))

    # Build feature paths
    args.features = args.features.split(',')
    feature_paths = args.features and [os.path.join('features', f) for f in args.features]
    for f in feature_paths:
        assert os.path.exists(f), 'Feature file "%s" not found in project/' % f

    for command in command_list:
        if getattr(args, command):
            print command
            try:
                command_mains[command](common_args, v1m, v1config, feature_paths)
            except AssertionError as exc:
                print 'Call "' + command + '" failed with message: ' + exc.message

    if not args.sync_only:
        sys.argv = [sys.argv[0]] + run_scenarios_args
        run_scenarios(run_scenarios_args)

    if args.update_results is not None:
        main_update_results(common_args + [args.update_results], v1m, v1config)


if __name__ == '__main__':
    main()
