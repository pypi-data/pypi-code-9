""" Creates a test set on V1 and updates the test results
"""
__author__ = 'mjhunick'

from helpers import results_dir, is_reg_test_number, get_html_results, \
    is_reg_suite_number, is_test_set_number
from v1pysdk import V1Meta
from configobj import ConfigObj
import argparse
import json
import ssl
import sys
import os
from time import strftime


def update_regression_results(v1config, results, test_suite_id=None, test_set_id=None, v1m=None):
    """
    :param v1config:
    :param results:
    :param test_suite_id:
    :param test_set_id:
    :param v1m:
    :return:
    """
    os.environ['OUTPUT'] = results_dir(v1config['yarara_base_dir'])  # Parametrize yarara functions
    status_codes = v1config['status_codes']

    if test_set_id is not None:
        try:
            test_set = next(iter(v1m.TestSet.where(Number=test_set_id)))
        except StopIteration:
            test_set = None
            assert 0, 'Test set does not exist in VersionOne'
    else:
        try:
            reg_suite = next(iter(v1m.RegressionSuite.where(Number=test_suite_id)))
        except StopIteration:
            reg_suite = None
            assert 0, 'Suite does not exist in VersionOne'

        assert 'test_set_prefix' in v1config, 'No test_set_prefix in config'
        prefix = v1config['test_set_prefix']
        v1m.TestSet.select('Name')
        # current time and date
        current_time = strftime('%Y-%m-%dT%H:%M:%S')
        new_name = prefix + " " + current_time
        print 'Creating new test set: ' + new_name
        test_set = v1m.TestSet.create(RegressionSuite=reg_suite,
                                      Name=new_name,
                                      Scope=reg_suite.SecurityScope)
        print 'Adding acceptance tests to test set'
        test_set.CopyAcceptanceTestsFromRegressionSuite()

    print 'Updating tests'
    for feature in results['features']:
        for scenario in feature['scenarios']:
            if str(scenario['status']) in ['passed', 'failed']:
                test_tags = [tag for tag in scenario['tags'] if is_reg_test_number(tag)]
                if len(set(test_tags)) > 1:
                    print 'Waring: More than one test tag for scenario ' + scenario['name']
                    continue
                if not test_tags:
                    continue
                tag = str(test_tags[0])
                status = str(scenario['status'])
                if status not in status_codes:
                    continue

                try:
                    print 'Updating test ' + tag
                    test = next(iter(v1m.Test.where(terms={
                        'Parent.Number': test_set.Number,
                        'GeneratedFrom.Number': tag
                    })))
                    test.Status = v1m.TestStatus(int(status_codes[status]))
                    test.ActualResults = get_html_results(scenario)
                except StopIteration:
                    print 'Test ' + tag + 'not found in test set'

    print 'Committing changes'
    v1m.commit()


def main(argm=sys.argv, v1m=None, v1config=None):
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

    parser.add_argument('tag', help='Tag of regression suite or test set')

    args = parser.parse_args(argm[1:])
    v1config['username'] = args.username
    v1config['password'] = args.password
    v1config['yarara_base_dir'] = args.yarara_dir

    if is_reg_suite_number(args.tag):
        args.test_suite_id = args.tag
        args.test_set_id = None
    elif is_test_set_number(args.tag):
        args.test_suite_id = None
        args.test_set_id = args.tag
    else:
        assert 0, 'Unrecognized tag: %s. Non regression suite id nor test set id'

    for attr in ['instance_url', 'status_codes']:
        assert attr in v1config, ('Missing attribute %s on versionone_config.cfg' % attr)

    results = None
    try:
        with open(os.path.join(results_dir(v1config['yarara_base_dir']), 'results.json')) \
                as results_file:
            results = json.load(results_file)
    except IOError:
        assert 0, 'Missing json results'
    except ValueError:
        assert 0, 'Malformed json results'

    update_regression_results(v1config, results, args.test_suite_id, args.test_set_id, v1m)


if __name__ == '__main__':
    main()
