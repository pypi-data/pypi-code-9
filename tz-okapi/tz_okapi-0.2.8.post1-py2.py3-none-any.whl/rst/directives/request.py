from collections import OrderedDict
import copy
import re

from docutils.nodes import Text
from docutils.parsers.rst.directives.body import CodeBlock

from okapi.core.request import Request, PrototypeRequest
from okapi.core.tests import Test
from okapi.rst.nodes import request_block
from okapi.settings import settings
from okapi.core.utils import RE_HEADER


METHOD_CLASS = {
    'post': 'success',
    'put': 'warning',
    'get': 'primary',
    'delete': 'danger',
}


class RequestDirective(CodeBlock):
    """
    Extends RST with request directive.

    Usage::

        .. code:: request

            GET /api/note/12/
            Authentication: topsecretpass

            > status_code == 200

    """

    re_request = re.compile(
        r'^(?P<method>GET|POST|PUT|PATCH|DELETE|OPTIONS|HEAD|TRACE|CONNECT) '
        r'(?P<url>[^ ]+)'
    )
    """ Regex to parse method and url from request line. """

    re_url = re.compile('{(?P<name>[^:]+):(?P<value>[^}]+)}')
    """
    Regex to parse url described with params. Spaces are not allowed.

    Example:

        /api/test/{userId:1}/{threadId:5}/

    """

    template_name = 'request.html'

    def __init__(self, *args, **kwargs):
        self.url = ''
        self.log = ''
        self.status = True
        """ URL of request. If described contains HTML tags. """

        self.request_cls = \
            Request if not settings.prototype else PrototypeRequest

        super(RequestDirective, self).__init__(*args, **kwargs)

    def get_breadcrumbs(self, node=None):
        """
        Get recursive titles of parent nodes and create breadcrumbs navigation.

        :return: Breadcrumbs string (eg. ``top > second title > third level``)
        :rtype: str
        """
        ret = ''

        if not node:
            node = self.state.parent

        if node.parent:
            ret = self.get_breadcrumbs(node.parent)

        value = node.attributes['names'][0] if node.attributes['names'] else ''

        return ret + (' > ' if ret else '') + value

    def run(self):
        """
        Parse request from source.

        :return: List of nodes
        :rtype: list[request_block]
        """
        breadcrumbs = self.get_breadcrumbs()

        if settings.internal.last_breadcrumb != breadcrumbs:
            self.log += '\n' + breadcrumbs.upper() + '\n'
            settings.internal.last_breadcrumb = breadcrumbs

        request = self.parse_request(copy.deepcopy(self.content))

        if not request:
            return []

        settings.internal.summary.count += 1
        self.log += '\t' + str(self.lineno) + ': '
        self.log += '{} {}'.format(request.method, request.url) + '\n'
        if request.cached:
            self.log += '\t\t[CACHED]'
        elif not request.run_tests():
            settings.internal.summary.failed += 1
            settings.internal.summary.failed_tests.append([
                self.lineno, request.method, request.url
            ])
            self.status = settings.internal.status = False

        template = settings.template.env.get_template(self.template_name)

        rendered = template.render(
            request=request,
            response=request.response,
            css_class=self.get_class(request),
            url=self.url,
        )
        node = request_block(request, rendered, Text(rendered))

        self.log += request.log
        self.print_log()
        return [node]

    def parse_request(self, content):
        """
        :type content: docutils.statemachine.StringList
        """
        headers = OrderedDict()
        payload = ''
        tests = []
        request_line = content.pop(0)
        request = self.re_request.match(request_line)
        try:
            method, url = request.group('method'), request.group('url')
        except AttributeError:
            settings.log.error(
                'Could not parse request line `{}`'.format(request_line)
            )
            settings.internal.status = False
            return

        url = self.parse_url(url)

        while content and RE_HEADER.match(content[0]):
            header = RE_HEADER.match(content.pop(0))
            headers[header.group('key')] = header.group('value')

        while content and not content[0].startswith('>'):
            payload += content.pop(0) + '\n'

        while content and content[0].startswith('>'):
            tests.append(Test(content.pop(0)[2:]))

        return self.request_cls(method, url, headers, payload, tests)

    def parse_url(self, s):
        self.url = self.re_url.sub(
            r'<abbr data-toggle="tooltip" data-placement="top" '
            r'title="\g<name>">\g<value></abbr>', s
        )
        url = self.re_url.sub(r'\g<value>', s)
        return url

    @staticmethod
    def get_class(request):
        return METHOD_CLASS.get(request.method, 'default')

    def print_log(self):
        if self.status:
            settings.log.success(self.log)
        else:
            settings.log.error(self.log)
