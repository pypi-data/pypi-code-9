import json
import os
import pexpect

_shared = {}


def get_pipeserver():
    server = _shared.get('SERVER')

    if server is None:
        server = launch_pipeserver()

    return server


def launch_pipeserver():
    extractor = os.path.join(os.path.dirname(__file__), './index.js')
    server = pexpect.spawn('node', [extractor])
    server.expect('PYBABEL_HTMLBARS RESPONSE:WAITING FOR COMMAND', timeout=3)
    _shared['SERVER'] = server

    return server


def extract_htmlbars(fileobj, keywords=None, comment_tags=None, options=None):
    """Extract messages from HTMLBars templates.

    It returns an iterator yielding tuples on the following form:
    ``(lineno, funcname, message, comments)``.
    """
    server = get_pipeserver()
    server.sendline('PYBABEL_HTMLBARS COMMAND:PARSE FILE:' + fileobj.name)
    server.expect('PYBABEL_HTMLBARS RESPONSE:SENDING OUTPUT')
    server.expect('PYBABEL_HTMLBARS RESPONSE:OUTPUT END')
    translatable_strings = server.before

    for item in json.loads(translatable_strings):
        messages = [item['content']]

        if 'alt_content' in item:
            messages.append(item['alt_content'])

        yield item['line_number'], item['funcname'], tuple(messages), []
