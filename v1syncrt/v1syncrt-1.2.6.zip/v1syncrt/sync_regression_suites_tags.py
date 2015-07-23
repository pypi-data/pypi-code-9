"""Adds tags from the corresponding suits to the tests on Yarara"""
__author__ = 'mjhunick'

from helpers import FeatureWrapper, is_reg_suite_number, \
    is_reg_test_number, get_features_paths, feature_dir
from configobj import ConfigObj
from v1pysdk import V1Meta
import ssl
import sys
import argparse


def sync_regression_suites_tags(v1config, feature_paths, v1m=None):
    """
    :param v1config:
    :param feature_paths:
    :param v1m:
    :return:
    """
    if v1m is None:
        v1m = V1Meta(instance_url=v1config['instance_url'],
                     username=v1config['username'],
                     password=v1config['password'])
    v1m.RegressionSuite.select('Number')
    for path in feature_paths:
        print 'Parsing feature ' + path
        feature = FeatureWrapper(path)
        if feature.feature is None:
            continue
        for scenario in feature.scenarios:
            test_tags = [tag for tag in scenario.tags if is_reg_test_number(tag)]
            if len(set(test_tags)) > 1:
                print 'Warning: More than one test tag for scenario ' + scenario['name']
                continue
            if not test_tags:
                continue
            tag = str(test_tags[0])
            try:
                test = next(iter(v1m.RegressionTest.where(Number=tag)))
            except StopIteration:
                continue
            print 'Updating suites of test ' + tag
            for t in scenario.tags:
                if is_reg_suite_number(t):
                    scenario.remove_tag(t)  # remove existing suite tags

            for suite in test.RegressionSuites:
                scenario.add_tag(suite.Number)

        feature.dump_to_file()


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

    for attr in ['instance_url']:
        assert attr in v1config, ('Missing attribute %s on versionone_config.cfg' % attr)

    feature_paths = feature_paths or get_features_paths(feature_dir(v1config['yarara_base_dir']))

    if not feature_paths:
        assert 0, 'Could not find any feature file'

    sync_regression_suites_tags(v1config, feature_paths, v1m)


if __name__ == '__main__':
    main()
