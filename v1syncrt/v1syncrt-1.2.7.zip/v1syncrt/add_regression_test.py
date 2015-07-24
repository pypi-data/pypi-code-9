""" Script for adding a regression test"""
__author__ = 'glucero'

from helpers import FeatureWrapper, \
    is_reg_test_number, get_features_paths, \
    feature_dir, sync_single_test
from configobj import ConfigObj
from v1pysdk import V1Meta
import ssl
import sys
import argparse


def sync_regression_test(v1config, feature_paths, v1m=None):
    """Sync Regression Tests """
    if v1m is None:
        # Open version one sdk
        v1m = V1Meta(instance_url=v1config['instance_url'],
                     username=v1config['username'], password=v1config['password'])

    # Look for the scope of the project.
    try:
        scope = next(iter(v1m.Scope.where(Name=v1config['project'])))
    # If the project name doesnt exits its an error.
    except StopIteration:
        scope = None
        assert 0, 'There is no Scope with name: ' + v1config['project']

    # Go through all the features file.
    for path in feature_paths:
        print 'Parsing feature ' + path
        feature = FeatureWrapper(path)
        if feature.feature is None:
            continue
        # Go through all the scenarios in the feature file.
        for scenario in feature.scenarios:
            # Check if the scenario has the tag to add to version one
            if v1config["tag_to_add_regression"] in scenario.tags:
                if not scenario.name:
                    print 'Error: Unnamed scenario'
                    continue

                # If the Scenario also has a tag of a regression test its an error.
                reg_tags = [tag for tag in scenario.tags if is_reg_test_number(tag)]
                if len(set(reg_tags)) != 0:
                    print 'Error: The scenario "' + scenario.name + \
                          '" has a tag of a regression' \
                        ' test and the tag: ' + v1config["tag_to_add_regression"]
                    continue

                # Create the regression test.
                regression_test = v1m.RegressionTest.create(Name=scenario.name, Scope=scope)

                # Change the tag "tag_to_add_regression" for the tag of the regression test.
                tag = regression_test.Number
                scenario.add_tag(tag)
                scenario.remove_tag(v1config["tag_to_add_regression"])

                sync_single_test(regression_test, scenario)
                # Tag to put in scenario
                print "\n Regression test: " + tag + " created.\n"

        feature.dump_to_file()

    print 'Committing to VersionOne'
    v1m.commit()


def main(argm=sys.argv, v1m=None, v1config=None, feature_paths=None):
    """ Creates the config and retrieves features paths"""
    if v1config is None:
        v1config = ConfigObj('versionone_config.cfg')
        v1config.setdefault('yarara_base_dir', '../../')

    # Check if the username and password is in the parameters
    parser = argparse.ArgumentParser()
    if 'username' in v1config:
        parser.add_argument('-u', '--username',
                            required=False, help='The username of VersionOne Client.',
                            default=v1config['username'])
    else:
        parser.add_argument('-u', '--username',
                            required=True, help='The username of VersionOne Client.')
    if 'password' in v1config:
        parser.add_argument('-p', '--password', required=False,
                            help='The password of VersionOne Client.', default=v1config['password'])
    else:
        parser.add_argument('-p', '--password',
                            required=True, help='The password of VersionOne Client.')
    if 'yarara_base_dir' in v1config:
        parser.add_argument('--yarara_dir', required=False,
                            help='Base directory of Yarara project',
                            default=v1config['yarara_base_dir'])
    else:
        parser.add_argument('--yarara_dir', required=True, help='Base directory of Yarara project')

    args = parser.parse_args(argm[1:])
    v1config['username'] = args.username
    v1config['password'] = args.password
    v1config['yarara_base_dir'] = args.yarara_dir

    feature_paths = feature_paths or get_features_paths(feature_dir(v1config['yarara_base_dir']))

    if not feature_paths:
        assert 0, 'Could not find any feature file'

    sync_regression_test(v1config, feature_paths, v1m)


if __name__ == '__main__':
    main()
