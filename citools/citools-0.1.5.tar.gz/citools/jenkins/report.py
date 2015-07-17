import json
import requests
from ..data import TestSuite, TestCase, TestReport


class Report(object):
    CASE_MAP = {'skipped': None, 'failedSince': None, 'className': 'classname', 'age': None}
    SUITE_MAP = {'timestamp': None, 'cases': 'testcases', 'id': None}

    API_JSON = "/api/json"

    def get_report(self, job_url, build_number=None):
        print job_url + self.API_JSON
        project_info = json.loads(requests.get(job_url + self.API_JSON).text)

        if build_number is None:
            build_number = project_info['lastCompletedBuild']['number']
        else:
            build_number = int(build_number)

        build_url = next(
            iter([build['url'] for build in project_info['builds'] if build['number'] == build_number]), None)

        if build_url is None:
            raise ValueError("no build with number {} found".format(build_number))

        build_info = json.loads(requests.get(build_url + self.API_JSON).text)

        print build_url + '/testReport' + self.API_JSON

        test_report_request = requests.get(build_url + '/testReport' + self.API_JSON)

        if test_report_request.status_code != 200:
            return None

        test_report = json.loads(test_report_request.text)

        suites_by_module = {}

        for child_report in test_report['childReports']:
            child_result = child_report['result']
            module_url = child_report['child']['url']
            module = module_url[len(job_url):].split('/')[1].replace('$', ':')
            suites = [self.create_suite(suite) for suite in child_result['suites']]
            suites_by_module[module] = suites

        is_incremental = bool([cause for cause in self.get_causes(build_info['actions'])
                              if cause['shortDescription'] == "Started by an SCM change"])

        return TestReport(build_info['displayName'], suites_by_module,
                          build_number, is_incremental)

    def create_suite(self, suite_properties):
        suite_properties = self.map_keys(suite_properties, self.SUITE_MAP)

        testcases = [self.create_case(case) for case in suite_properties['testcases']]
        suite_properties['testcases'] = testcases
        suite_properties['passed'] = len([testcase for testcase in testcases if testcase.status == 'PASSED'])
        suite_properties['skipped'] = len([testcase for testcase in testcases if testcase.status == 'SKIPPED'])
        suite_properties['failures'] = len([testcase for testcase in testcases if testcase.status == 'FAILED'])
        suite_properties['errors'] = len([testcase for testcase in testcases if testcase.status == 'ERROR'])

        return TestSuite(**suite_properties)

    def create_case(self, case_properties):
        case_properties = self.map_keys(case_properties, self.CASE_MAP)
        return TestCase(**case_properties)

    def map_keys(self, target, key_map):
        for old_key, new_key in key_map.iteritems():
            value = target.pop(old_key)
            if value is not None and new_key is not None:
                target[new_key] = value
            elif new_key is None:
                print("dropped {}: {}".format(old_key, value))

        return target

    def get_causes(self, actions):
        for action in actions:
            if 'causes' in action:
                return action['causes']
        return []
