""" Adds tags of test to its corresponding regression test on V1"""
__author__ = 'glucero'

from helpers import FeatureWrapper, \
    is_reg_test_number, get_features_paths, feature_dir, sync_single_test
from configobj import ConfigObj
from v1pysdk import V1Meta
import ssl
import argparse
import sys


def sync_tags(v1config, feature_paths, v1m=None):
    """
    :param v1config:
    :param feature_paths:
    :param v1m:
    :return:
    """
    if v1m is None:
        # Open version one sdk
        v1m = V1Meta(instance_url=v1config['instance_url'],
                     username=v1config['username'],
                     password=v1config['password'])

    # Go through all the features file.
    for path in feature_paths:
        print 'Parsing feature ' + path
        feature = FeatureWrapper(path)
        if feature.feature is None:
            continue
        # Go through all the scenarios in the feature file.
        for scenario in feature.scenarios:
            # Check if the scenario has regression test tag.
            reg_tags = [tag for tag in scenario.tags if is_reg_test_number(tag)]
            if len(set(reg_tags)) == 0:
                print 'The Scenario: "' + scenario.name + '" doesnt have a regression test tag.\n'
                continue

            if len(set(reg_tags)) > 1:
                print 'The Scenario: "' + scenario.name + '" has more than 1 regression test tag.\n'
                continue

            # Look for the regression test.
            try:
                test = next(iter(v1m.RegressionTest.where(Number=reg_tags[0]).select('Tags')))
            # If the regression test doesnt exist
            except StopIteration:
                print 'The Scenario: "' + scenario.name + '" has a regression test tag: "' \
                      + str(reg_tags[0]) + '" that doesnt exist in version one.\n'
                continue

            # Update regression test.
            print 'Updating regression test: "' + str(test.Number) + '"'
            try:
                sync_single_test(test, scenario)
            except ValueError:
                print 'Error updating test "' + str(test.Number) + '"'


    print 'Doing commit into version one.\n'
    v1m.commit()


def main(argm=sys.argv, v1m=None, v1config=None, feature_paths=None):
    """Takes config from calls and config file"""
    if v1config is None:
        v1config = ConfigObj('versionone_config.cfg')
        v1config.setdefault('yarara_base_dir', '../../')

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
    if 'yarara_base_dir' in v1config:
        parser.add_argument('--yarara_dir', required=False,
                            help='Base directory of Yarara project',
                            default=v1config['yarara_base_dir'])
    else:
        parser.add_argument('--yarara_dir', required=True,
                            help='Base directory of Yarara project')

    args = parser.parse_args(argm[1:])
    v1config['username'] = args.username
    v1config['password'] = args.password
    v1config['yarara_base_dir'] = args.yarara_dir

    feature_paths = feature_paths or get_features_paths(feature_dir(v1config['yarara_base_dir']))

    if not feature_paths:
        assert 0, 'Could not find any feature file'

    sync_tags(v1config, feature_paths, v1m)


if __name__ == '__main__':
    main()
