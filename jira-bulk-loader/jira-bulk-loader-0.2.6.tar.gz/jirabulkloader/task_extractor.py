# -*- coding: UTF-8 -*-

import re
import simplejson as json
from task_extractor_exceptions import TaskExtractorTemplateErrorProject, TaskExtractorTemplateErrorJson, TaskExtractorJiraValidationError
from jiraConnect import JiraConnect, JiraConnectActionError


class TaskExtractor:

    def __init__(self,
                 jira_url,
                 username,
                 password,
                 options={},
                 dry_run=False):
        self.tmpl_vars = {}  # template variables dict
        self.tmpl_json = {}  # template json structures
        self.rt_vars = {}    # run-time variables (issueIDs)
        self.links = []      # to keep link info

        self.default_params = options
        self.dry_run = dry_run

        self.jira_connect = JiraConnect(self._validate_url_and_type(jira_url),
                                        username,
                                        password)


# ###################################################################################
# helpers for validate_load()

    def _validate_url_and_type(self, url):
        match = re.search("^https?://", url)
        return url if match else "http://" + url

# end of load() helpers
# ###################################################################################

    def validate_load(self, task_list):
        """
        Take the task_list prepared by load() and validate assignees and projects
        """
        assignees = []

        for line in task_list:
            if 'assignee' in line:
                if line['assignee'] not in assignees:
                    assignees.append(line['assignee'])
                    self._validate_user(
                        line['assignee'],
                        self._get_project_or_raise_exception(line))


# ###################################################################################
# helpers for validate_load()

    def _get_project_or_raise_exception(self, input_line):
        try:
            return input_line['tmpl_ext']['project']['key']
        except KeyError:
            if 'project' in self.default_params:
                return self.default_params['project']['key']
            else:
                raise TaskExtractorTemplateErrorProject('Missing project key in line: ' + input_line['summary'] \
                        + '.\nYou should add \'{"project": {"key": "JIRA"}}\' to the template, where "JIRA" must be replaced by your real project key.')

    def _validate_user(self, user, project):
        """
        Checks if a new issue of the project can be assigned to the user.
        http://docs.atlassian.com/jira/REST/latest/#id120417
        """

        full_url = "user/assignable/search?username={0}&project={1}".format(user, project)
        try:
            self.jira_connect.get('user/assignable/search', username=user, project=project)
        except JiraConnectActionError, e:
            if e.code == 403 or e.code == 401:
                error_message = "Your username and password are not accepted by Jira."
                raise TaskExtractorJiraValidationError(error_message)
            else:
                raise TaskExtractorJiraValidationError(e.message)
#        try:
#            res = self._jira_request(full_url, None, 'GET')
#            print res
#            result = json.loads(res)
#        except URLError, e:
#            if hasattr(e, 'code'):
#                if e.code == 403 or e.code == 401:
#                    error_message = "Your username and password are not accepted by Jira."
#                    raise TaskExtractorJiraValidationError(error_message)
#                else:
#                    error_message = "The username '%s' and the project '%s' can not be validated.\nJira response: Error %s, %s" % (user, project, e.code, full_url) #e.read())
#                    raise TaskExtractorJiraValidationError(error_message)
#            elif hasattr(e, 'reason'):
#                error_message = "%s: %s" % (e.reason, self.jira_url)
#                raise TaskExtractorJiraHostProblem(error_message)
#        if len(result) == 0: # the project is okay but username is missing n Jira
#            error_message = "ERROR: the username '%s' specified in template can not be validated." % user
#            raise TaskExtractorJiraValidationError(error_message)


# end of load() helpers
###############################################################################

    def load(self, input_text):
        """
        Parse and convert the input_text to a list of tasks
        """
        result = []
        line_number = 1

        pattern_task = re.compile('^(h5\.|h4\.|#[*#]?|\(-\))\s+(.+)\s+\*([_\-A-z]+)\*(.*)')
        pattern_vars = re.compile('^\[(\w+)=(.+)\]$')
        pattern_json = re.compile('^{.+}$')
        pattern_existing_task = re.compile('^(\.{2,3})\s([A-Z].+\-\d.+)$')

        for line in input_text.splitlines():
            if self.tmpl_vars:
                line = self._replace_template_vars(line)
            line = line.rstrip()
            if line.startswith(('h', '#', '(')):
                match_task = pattern_task.search(line)
                if match_task:
                    result.append(self._make_json_task(match_task))
                    result[-1]['line_number'] = line_number
                    line_number += 1
                    continue

            if line.startswith('='):  # if description
                result[-1] = self._add_task_description(result[-1], line[1:])
                line_number += 1
                continue

            if line.startswith('.'):
                match = pattern_existing_task.search(line)
                if match:
                    result.append(self._make_existing_task(match))
                    result[-1]['line_number'] = line_number
                    line_number += 1
                    continue

            if line.startswith(('[', '{')):
                match_vars = pattern_vars.search(line)
                if match_vars:
                    self._add_template_variable(
                        match_vars.group(1), match_vars.group(2))
                else:
                    if pattern_json.match(line):  # if json
                        self.tmpl_json.update(self._validated_json_loads(line))
                line_number += 1
                continue

            if len(result) > 0:
                result.append({'text': line})
            line_number += 1

        return result

###############################################################################
# several helpers for load()

    def _make_existing_task(self, match):
        task_json = {'markup': match.group(1), 'issue_key': match.group(2)}
        return task_json

    def _make_json_task(self, match):
        task_json = {'markup': match.group(1),
                     'summary': match.group(2),
                     'assignee': match.group(3)}
        if len(self.tmpl_json) != 0:
            task_json['tmpl_ext'] = self.tmpl_json.copy()
        if match.group(4):
            self._add_task_options(task_json, match.group(4))
        return task_json

    def _add_task_options(self, task_json, options):
        m = re.match('\s+%(\d{4}-\d\d-\d\d)%', options)
        if m:
            task_json['duedate'] = m.group(1)
        m = re.match('.+({.+})', options)
        if m:
            task_json.setdefault(
                'tmpl_ext', {}).update(self._validated_json_loads(m.group(1)))
        m = re.match('.+\[(\w+)\]', options)
        if m:
            task_json['rt_ext'] = m.group(1)
        m = re.match('.+<(.+|.+)>', options)
        if m:
            task_json['link'] = m.group(1)
        return task_json

    def _add_task_description(self, task_json, input_line):
        desc = 'description'
        task_json[desc] = \
            '\n'.join([task_json[desc], input_line]) \
            if task_json.get(desc) else input_line
        return task_json

    def _replace_template_vars(self, input_line):
        return self.tmpl_vars_regex.sub(
            lambda match: self.tmpl_vars[match.group(1)], input_line)

    def _add_template_variable(self, name, value):
        self.tmpl_vars[name] = value
        # here I recompile template vars regex
        # sorted() is used to put vars with longer names at the beginning of
        # regex otherwise vars with similar names will not be replaced
        # as '|' is not greedy
        self.tmpl_vars_regex = \
            re.compile("\$(" + "|".join(map(re.escape,
                       sorted(self.tmpl_vars.keys(), reverse=True))) + ")")

    def _validated_json_loads(self, input_line):
        result = ''
        try:
            result = json.loads(input_line)
        except json.JSONDecodeError:
            raise TaskExtractorTemplateErrorJson(input_line)
        return result

# end of load() helpers
###############################################################################

    def jira_format(self, task):
        fields = {}

        fields.update(self.default_params)
        if 'tmpl_ext' in task:
            fields.update(task['tmpl_ext'])
        if 'duedate' in task:
            fields['duedate'] = task['duedate']
        fields['summary'] = task['summary']
        if 'description' in task:
            fields['description'] = task['description']
        fields['issuetype'] = {'name': task['issuetype']}
        fields['assignee'] = {'name': task['assignee']}
        if 'parent' in task:
            fields['parent'] = {'key': task['parent']}

        return {'fields': fields}

    def create_tasks(self, task_list):
        """
        It takes the task_list prepared by load(), creates all tasks
        and compose created tasks summary.
        """

        summary = []
        args = {}
        actions = {
            'h4.': self._create_h4_task,
            '..': self._attach_h4_task,
            'h5.': self._create_h5_task,
            '...': self._attach_existing_h5_task,
            '(-)': self._create_sub_task,
            '#': self._create_sub_task,
            '#*': self._create_sub_task
        }

        for line in task_list:
            if 'markup' in line:
                if 'description' in line:
                    line['description'] = \
                        self._replace_realtime_vars(line['description'])
                summary.extend(actions[line['markup']](line, args))
            elif 'text' in line:
                summary.append(line['text'])
                if 'h5_task_desc' in args:
                    args['h5_task_desc'].append(line['text'])

        if 'h5_task_key' in args:
            self._h5_task_completion(args)

        for link in self.links:
            self.create_link(self._replace_realtime_vars(link['inward']),
                             self._replace_realtime_vars(link['outward']),
                             link['type'])

        return '\n'.join(summary)

# ###################################################################################
# several helpers for create_tasks()

    def _make_task_caption(self, task_json, task_key):
        return u' '.join([
            task_json['markup'],
            task_json['summary'], '(' + task_key + ')'])

    def _h5_task_completion(self, args):
        desc = ''
        len_args = len(args['h5_task_desc'])
        if len_args > 0:
            desc = self._replace_realtime_vars('\n'.join(args['h5_task_desc']))
        if len_args > args['h5_task_desc_len']:
            self.update_issue_desc(args.get('h5_task_key'), desc)
        args.pop('h5_task_key', None)
        args.pop('h5_task_desc', None)
        return desc

    def _create_sub_task(self, task_json, args):
        task_json['parent'] = \
            args.get('h5_task_key') or args.get('h4_task_key')
        task_json['issuetype'] = u'Sub-task'
        task_key = self.create_issue(task_json)
        desc = self._make_task_caption(task_json, task_key)
        if 'h5_task_key' in args:
            args['h5_task_desc'].append(desc)
        return [desc]

    def _create_h5_task(self, task_json, args):
        if 'h5_task_key' in args:  # if new h5 task begins
            self._h5_task_completion(args)
        task_json['issuetype'] = u'Task'
        key = self.create_issue(task_json)
        args['h5_task_key'] = key
        args['h5_task_desc'] = []
        if 'description' in task_json:
            args['h5_task_desc'].append(task_json['description'])
        args['h5_task_desc_len'] = len(args['h5_task_desc'])
        if args.get('h4_task_key') is not None:
            self.create_link(args.get('h4_task_key'), key)
        desc = [self._make_task_caption(task_json, key)]
        desc.extend(args['h5_task_desc'])
        return desc

    def _attach_existing_h5_task(self, task_json, args):
        if 'h5_task_key' in args:  # if new h5 task begins
            self._h5_task_completion(args)
        task_json['issuetype'] = u'Task'
        key = task_json['issue_key']
        args['h5_task_key'] = key
        if 'h4_task_key' in args:
            self.create_link(args['h4_task_key'], key)
        args['h5_task_desc'] = [task_json['description']] \
            if 'description' in task_json else []
        args['h5_task_desc_len'] = len(args['h5_task_desc'])
        desc = [u' '.join((task_json['markup'], key))]
        desc.extend(args['h5_task_desc'])
        return desc

    def _create_h4_task(self, task_json, args):
        task_json['issuetype'] = u'User Story'
        args['h4_task_key'] = self.create_issue(task_json)
        return [self._make_task_caption(task_json,  args['h4_task_key'])]

    def _attach_h4_task(self, task_json, args):
        args['h4_task_key'] = task_json['issue_key']
        return [u'.. ' + task_json['issue_key']]

# end of create_tasks() helpers
# ###################################################################################

    def create_issue(self, issue):
        if ('description' in issue) and self.rt_vars:
            issue['description'] = \
                self._replace_realtime_vars(issue['description'])
        issue_id = self._create_issue_http(issue)
        if 'rt_ext' in issue:
            self._add_runtime_variable(issue['rt_ext'], issue_id)
        if 'link' in issue:
            self._add_link_info(issue_id, issue['link'])
        return issue_id

    def _add_link_info(self, issue_id, link_pattern):
        m = re.match('([A-Z]+-\d+|\$\w+)\|(.+)', link_pattern)
        if m:
            self.links.append({'inward': m.group(1),
                               'type': m.group(2),
                               'outward': issue_id})
        m = re.match('(.+)\|([A-Z]+-\d+|\$\w+)', link_pattern)
        if m:
            self.links.append({'inward': issue_id,
                               'type': m.group(1),
                               'outward': m.group(2)})
        m = re.match('^([A-Z]+-\d+|\$\w+)$', link_pattern)
        if m:
            self.links.append({'inward': issue_id,
                               'type': 'Inclusion',
                               'outward': m.group(1)})
        # TODO: check if there is no match

    def _add_runtime_variable(self, name, value):
        self.rt_vars.update({name: value})
        self.rt_vars_regex = \
            re.compile("\$(" + "|".join(map(re.escape,
                       sorted(self.rt_vars.keys(), reverse=True))) + ")")

    def _replace_realtime_vars(self, desc):
        return self.rt_vars_regex.sub(
            lambda match: self.rt_vars[match.group(1)], desc) \
            if self.rt_vars else desc

    def _create_issue_http(self, issue):
        """
        Invoke JIRA HTTP API to create issue
        """

        if not self.dry_run:
            try:
                jira_response = self.jira_connect.post('issue', json.dumps(self.jira_format(issue)))
                issueID = json.loads(jira_response)
                return issueID['key']
            except JiraConnectActionError, e:
                error_message = "Can't create task in the line {0} of your template.\nJIRA error: {1}".format(issue['line_number'], e.message)
                raise TaskExtractorJiraValidationError(error_message)
        else:
            return 'DRYRUN-1234'

    def create_link(self, inward_issue, outward_issue, link_type='Inclusion'):
        """Creates an issue link between two issues.

        The specified link type in the request is used to create the link
        and will create a link from the inward_issue to the outward_issue.
        The list of issue types can be retrieved using rest/api/2/issueLinkType
        """

        if not self.dry_run:
            jira_link = {"type": {"name": link_type},
                         "inwardIssue": {"key": inward_issue},
                         "outwardIssue": {"key": outward_issue}}
            return self._jira_request('issueLink', json.dumps(jira_link))
        else:
            return 'dry run'

    def update_issue_desc(self, issue_key, issue_desc):
        if not self.dry_run:
            full_url = 'issue/' + issue_key
            jira_data = {'update': {'description': [{'set': issue_desc}]}}
            return self._jira_request(full_url, json.dumps(jira_data), 'PUT')
        else:
            return 'dry run'

    def _jira_request(self,
                      action,
                      data,
                      method='POST',
                      headers={'Content-Type': 'application/json'}):
        """Compose and make HTTP request to JIRA.

        url should be a string containing a valid URL.
        data is a str. headers is dict of HTTP headers.
        Supported method are POST (for creating and linking)
        and PUT (for updating).
        It expects also self.username and self.password to be set
        to perform basic HTTP authentication.
        """

        if method == 'POST':
            return self.jira_connect.post(action, data)
        elif method == 'GET':
            return self.jira_connect.get(action)
        elif method == 'PUT':
            return self.jira_connect.put(action, data)
