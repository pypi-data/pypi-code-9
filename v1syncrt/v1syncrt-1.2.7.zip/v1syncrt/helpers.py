"""
Helpers for VersionOne - Yarara synchronization
"""
__author__ = 'mjhunick'

import cgi
import os
import re
import types
from behave.model import Tag
from behave.parser import parse_feature, ParserError
from tabulate import tabulate
from yarara.reports.report_utils import gather_errors


class V1NumberMatcher(object):
    """
    Class for building matchers of VersionOne assets tags
    """
    def __init__(self, exp):
        self.matcher = re.compile(exp)

    def __call__(self, tag):
        match = self.matcher.match(tag)
        return match is not None and match.end() == len(tag)


is_reg_test_number = V1NumberMatcher('RT-[0-9]+')
is_reg_suite_number = V1NumberMatcher('RS-[0-9]+')
is_test_set_number = V1NumberMatcher('TS-[0-9]+')


def table_to_string(table):
    """
    Transforms a behave table to string
    """
    return tabulate([table.headings] + [row.cells for row in table.rows], tablefmt='orgtbl')


def example_to_string(example, tab='    '):
    """
    Transforms a behave example to string
    """
    result = 'Examples:'
    if example.name:
        result += ' ' + example.name
    if example.table:
        result += ('\n' + table_to_string(example.table)).replace('\n', '\n' + tab)
    return result


def step_to_string(step, tab='    '):
    """
    Transforms a behave step to string
    """
    result = step.keyword + ' ' + step.name
    if step.table:
        result += ':' + ('\n' + table_to_string(step.table)).replace('\n', '\n' + tab)
    return result


def steps_to_string(steps, tab='    '):
    """
    Transforms a behave list of steps to string
    """
    if not steps:
        return ''
    return '\n'.join(step_to_string(step, tab) for step in steps)


def background_to_string(background, tab='    '):
    """
    Transforms a behave background to string
    """
    result = ''
    result += 'Background:'
    if background.name:
        result += ' ' + background.name
    result += ('\n' + steps_to_string(background.steps, tab)).replace('\n', '\n' + tab)
    return result


def scenario_to_string(scenario, tab='    '):
    """
    Transforms a behave scenario to string
    """
    result = ''
    if scenario.tags:
        result += ' '.join(['@' + tag for tag in scenario.tags]) + '\n'
    if scenario.type == 'scenario':
        result += 'Scenario:'
    elif scenario.type == 'scenario_outline':
        result += 'Scenario Outline:'
    else:
        raise NotImplementedError
    if scenario.name:
        result += ' ' + scenario.name
    result += ('\n' + steps_to_string(scenario.steps, tab)).replace('\n', '\n' + tab)
    if scenario.type == 'scenario_outline' and scenario.examples:
        result += ('\n' + '\n'.join((example_to_string(ex, tab))
                                    for ex in scenario.examples)).replace('\n', '\n' + tab)
    return result


def feature_to_string(feature, tab='    '):
    """
    Transforms a behave feature to string
    """
    result = ''
    if feature.tags:
        result += ' '.join(['@' + tag for tag in feature.tags]) + '\n'
    result += 'Feature:'
    if feature.name:
        result += ' ' + feature.name
    result += '\n' + ('\n' + background_to_string(
        feature.background, tab)).replace('\n', '\n' + tab)

    if feature.scenarios:
        result += '\n' + '\n'.join(('\n' + scenario_to_string(sc, tab)).replace('\n', '\n' + tab)
                                   for sc in feature.scenarios)

    return result


def get_features_paths(base_dir='.'):
    """
    Returns the list of paths of features found in subdirectories of base_dir
    """
    feature_paths = []
    for (dir_path, _, filenames) in os.walk(base_dir):
        feature_paths += [os.path.join(dir_path, name)
                          for name in filenames if name.endswith('.feature')]
    return feature_paths


def escape_html(text):
    """
    Escapes special html characters and replaces new lines with <br/>
    """
    return cgi.escape(text).replace('\n', '<br/>')


def get_html_results(scenario):
    """
    Returns yarara report of scenario in html format
    """
    result = ''
    log_name = scenario['name'].replace(' ', '_')
    log_path = os.path.join(
        os.environ['OUTPUT'], 'reports/logs/' + log_name + '/' + log_name + '.log')
    error_msg, error_lines = gather_errors(scenario, False)
    html_test_log = ''
    if error_msg:
        html_test_log = '<strong>' + escape_html(error_msg) +\
                        '</strong>' + '<br/>'.join(escape_html(s) for s in error_lines)
    if html_test_log:
        result += '<br/><br/><h3>Error</h3>' + html_test_log
    try:
        with open(log_path) as log_file:
            result += '<h3>Log</h3>' + escape_html(log_file.read())
    except IOError:
        pass

    return result


def feature_dir(yarara_dir):
    """
    Returns features directory from yarara project directory
    """
    return os.path.join(yarara_dir, 'project/features/')


def results_dir(yarara_dir):
    """
    Returns features directory from yarara project directory
    """
    return os.path.join(yarara_dir, 'output/results/')


class FeatureWrapper(object):
    """
    Extends functionality of behave Feature.
    Allows adding and removing scenario's tags from code
    """
    def __init__(self, filename):
        self.filename = filename
        self.lines = []
        self.reload()

    def __getattr__(self, name):
        # If attribute not found return feature's attribute
        return self.feature.__getattribute__(name)

    def reload(self):
        """
        Reads feature from self.filename
        """
        with open(self.filename) as feature_file:
            data = feature_file.read().decode('utf-8')
        try:
            self.feature = parse_feature(data, filename=self.filename)
        except ParserError:
            self.feature = None
        if self.feature is None:
            return
        self.lines = data.split('\n')
        for scenario in self.feature.scenarios:
            # Extend functionality of scenarios
            scenario.feature = self
            scenario.add_tag = types.MethodType(add_scenario_tag, scenario)
            scenario.remove_tag = types.MethodType(remove_scenario_tag, scenario)

    def to_string(self):
        """
        Transforms feature to string
        """
        return '\n'.join(self.lines).encode('utf-8')

    def dump_to_file(self):
        """
        Dumps feature to self.filename
        """
        with open(self.filename, 'w') as feature_file:
            feature_file.write(self.to_string())

    def add_scenario(self, scenario, tab='    ', must_reload=True):
        """
        Adds scenario to feature and code
        """
        self.lines += [''] + [tab + line for line in scenario_to_string(scenario, tab).split('\n')]
        if must_reload:
            self.dump_to_file()
            self.reload()

    def add_scenarios(self, scenarios, must_reload=True):
        """
        Adds multiple scenarios to feature and code
        """
        for scenario in scenarios:
            self.add_scenario(scenario, must_reload=False)
        if must_reload:
            self.dump_to_file()
            self.reload()

    def remove_scenarios_with_tags(self, tags, must_reload=True):
        """
        Removes scenarios matching one or more of list tags
        """
        keep_line = [True for _ in xrange(len(self.lines))]
        for i, scenario in enumerate(self.scenarios):
            if set(tags) & set(scenario.tags):
                # remove
                first_line = min([scenario.line] + [t.line for t in scenario.tags]) - 1
                last_line = max([scenario.line] + [s.line for s in scenario.steps]) - 1
                # try to remove one more line (empty) for formatting
                if last_line < len(self.lines) - 1 and self.lines[last_line + 1].strip() == '':
                    last_line += 1
                elif self.lines[first_line - 1].strip() == '':
                    first_line -= 1
                for j in xrange(first_line, last_line + 1):
                    keep_line[j] = False
                # remove from scenarios list
                self.feature.scenarios = self.scenarios[:i] + self.scenarios[i + 1:]

        self.lines = [l for i, l in enumerate(self.lines) if keep_line[i]]

        if must_reload:
            self.dump_to_file()
            self.reload()


def add_scenario_tag(scenario, tag):
    """
    Adds tag to scenario and feature's code
    """
    feature = scenario.feature
    if tag in scenario.tags:
        return
    if not scenario.tags:
        tag_line = scenario.line
        tag = Tag(tag, tag_line)
        # Append new line with tag before scenario
        feature.lines.insert(tag_line - 1, '@' + tag)
        scenario.location.line += 1
        for other_scenario in feature.scenarios:
            if other_scenario is not scenario and other_scenario.line >= scenario.line:
                other_scenario.location.line += 1
                for tag in other_scenario.tags:
                    tag.line += 1
    else:
        line_number = scenario.tags[0].line
        line = feature.lines[line_number - 1]
        tag = Tag(tag, line_number)
        # Add tag before first tag
        tag_index = line.index('@')
        feature.lines[line_number - 1] = line[:tag_index] + '@' + tag + ' ' + line[tag_index:]

    scenario.tags.insert(0, tag)


def remove_scenario_tag(scenario, tag):
    """
    Removes tag from scenario and feature's code
    """
    feature = scenario.feature
    assert tag in scenario.tags
    tag_line = scenario.tags[scenario.tags.index(tag)].line
    i = feature.lines[tag_line - 1].find('@' + tag)
    if i > 0 and feature.lines[tag_line - 1][i-1] == ' ':
        feature.lines[tag_line - 1] = feature.lines[tag_line - 1].replace(' @' + tag, '', 1)
    else:
        feature.lines[tag_line - 1] = feature.lines[tag_line - 1].replace('@' + tag, '', 1)
    scenario.tags.remove(tag)


def sync_single_test(v1rt, scenario):
    new_name = scenario.name
    steps = scenario.steps
    setup = scenario.background.steps
    steps = escape_html(steps_to_string(steps))
    setup = escape_html(steps_to_string(setup))

    tags_to_add = list(scenario.tags)
    tags_to_add.remove(v1rt.Number)
    if v1rt.Tags is not None:
        tags_test = v1rt.Tags.split()
    else:
        tags_test = []
    tags = set(tags_to_add + tags_test)
    tags = " ".join(tags)

    v1rt.Name = new_name
    v1rt.Steps = steps
    v1rt.Setup = setup
    v1rt.Tags = tags
