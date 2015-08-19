"""
# handleget sourcecode -- please see handleget/readme.md
## src/parse.py
This file handles any code which is responable for parsing data. Most of that
code is contained withen the ParseHandler class.
"""

import json
import click

class ParseHandler(object):
    def __init__(self, error_handler, verbose=False):
        self.error_handler = error_handler
        self.verbose = verbose

    def parse_responses(self, services, responses):
        output = ""
        for s in services:
            if s['response_type'] == 'json':
                output += self._parse_response_json(s, responses[s['name']])
        return output

    def _parse_response_json(self, s, responses):
        output = ""
        for username in responses:
            output += '\n! '
            py_response = json.loads(responses[username])
            username_free = True
            for requirement in s['username_free']:
                for key in requirement:
                    if py_response[key] != requirement[key]:
                        username_free = False
            if username_free:
                output += '{0} available on {1}'.format(username, s['name'])
            else:
                output += '{0} taken/invalid on {1}'.format(username, s['name'])
            output += '\n'
        return output
