"""
# handleget sourcecode -- please see handleget/readme.md
## src/requrest.py

"""
import six.moves.urllib.request
import click

class RequestHandler(object):
    def __init__(self, error_handler, verbose=False):
        self.error_handler = error_handler
        self.verbose = verbose

    def _collect_service_responses(self, service, username_list):
        responses = {}
        if 'url' not in service:
            click.echo('That service is not configured correctly. Please double check!')
            return

        for username in username_list:
            formatted_url = service['url'].format(username)
            if self.verbose:
                print('!+ Making request to {0}'.format(formatted_url))
            response = six.moves.urllib.request.urlopen(formatted_url)
            str_response = response.read().decode('utf-8')
            responses[username] = str_response
        return responses

    def web_request(self, services, usernames):
        responses = {}
        for s in services:
            if self.verbose:
                click.echo('! Beginning collection for {0}'.format(s['name']))
            responses[s['name']] = self._collect_service_responses(s, usernames)
        return responses
