""" This script adds all the regression tests to the
suite they have been tagged
"""
__author__ = 'glucero'

from helpers import FeatureWrapper, \
    is_reg_suite_number, \
    is_reg_test_number, get_features_paths, feature_dir
from configobj import ConfigObj
from v1pysdk import V1Meta
import ssl
import sys
import argparse


def sync_test_suite(v1config, feature_paths, v1m=None):
    """ Sync test for every feature in feature_paths"""
    if v1m is None:
        # Open version one sdk
        v1m = V1Meta(instance_url=v1config['instance_url'],
                     username=v1config['username'],
                     password=v1config['password'])

    v1m.RegressionTest.select('Number')  # Cache regression test numbers
    # Go through all the features file.
    for path in feature_paths:
        print 'Parsing feature ' + path
        feature = FeatureWrapper(path)
        if feature.feature is None:
            continue
        # Go through all the scenarios in the feature file.
        for scenario in feature.scenarios:
            # Check if the scenario has regression suite tags.
            suite_tags = [tag for tag in scenario.tags if is_reg_suite_number(tag)]
            # If there is no regression suite tags do nothing.
            if len(set(suite_tags)) == 0:
                continue

            # If there is a regression suite tag
            # Check if the scenario has regression test tag.
            reg_tags = [tag for tag in scenario.tags if is_reg_test_number(tag)]
            if len(set(reg_tags)) == 0:
                print 'The Scenario: "' + scenario.name + '" has a regression suite tag but it' \
                                                          ' doesnt have any regression test tag.\n'
                continue

            if len(set(reg_tags)) > 1:
                print 'The Scenario: "' + scenario.name + '" has more than 1 regression test tag.\n'
                continue

            # Look for the regression test.
            try:
                test = next(iter(v1m.RegressionTest.where(Number=reg_tags[0])))
            # If the regression test doesnt exist
            except StopIteration:
                print 'The Scenario: "' + scenario.name + '" has a regression test tag: "' \
                      + str(reg_tags[0]) + '" that doesnt exist in version one.\n'
                continue

            for suite_tag in suite_tags:
                # Look for the regression suite.
                try:
                    suite = next(iter(v1m.RegressionSuite.where(Number=suite_tag)))
                # If the regression suite doesnt exist
                except StopIteration:
                    print 'The Scenario: "' + scenario.name + '" has a regression suite tag: "' \
                          + str(suite_tag) + '" that doesnt exist in version one.\n'
                    continue

                # Add regression test to suite.
                if test.Number not in [t.Number for t in suite.RegressionTests]:
                    print 'Adding regression test: "' + str(test.Number) \
                      + '" into regression suite: "' + suite.Number + '"\n'
                    suite.RegressionTests += [test]

    print 'Doing commit into version one.\n'
    v1m.commit()


def main(argm=sys.argv, v1m=None, v1config=None, feature_paths=None):
    """"Sets up variables and calls script"""
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

    sync_test_suite(v1config, feature_paths, v1m)


if __name__ == '__main__':
    main()
