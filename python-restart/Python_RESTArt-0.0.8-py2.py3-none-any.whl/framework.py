from __future__ import absolute_import

from werkzeug.routing import Map, Rule

from .request import Request, WerkzeugRequest
from .response import Response, WerkzeugResponse


class Adapter(object):
    """The adapter class for adapting the RESTArt API.

    :param api: the RESTArt API.
    """

    #: The class that is used for request objects.  See
    #: :class:`~restart.request.Request` for more information.
    request_class = Request

    #: The class that is used for response objects.  See
    #: :class:`~restart.response.Response` for more information.
    response_class = Response

    def __init__(self, api):
        self.api = api
        self.adapted_rules = self.adapt(api.rules)

    def adapt(self, rules):
        """Adapt the rules to be framework-specific."""
        def decorator(handler):
            def adapted_handler(request, *args, **kwargs):
                """Adapt the request object and the response object for
                each `handler` in `rules`.
                """
                adapted_request = self.request_class(request)
                response = handler(adapted_request, *args, **kwargs)
                adapted_response = self.response_class(
                    response.data, response.status, response.headers
                )
                return adapted_response.get_specific_response()
            return adapted_handler
        adapted_rules = {
            endpoint: decorator(handler)
            for endpoint, handler in rules.iteritems()
        }
        return adapted_rules

    @property
    def final_rules(self):
        raise NotImplementedError()


class WerkzeugAdapter(Adapter):

    #: The class that is used for request objects.  See
    #: :class:`~restart.request.WerkzeugRequest` for more information.
    request_class = WerkzeugRequest

    #: The class that is used for response objects.  See
    #: :class:`~restart.response.WerkzeugResponse` for more information.
    response_class = WerkzeugResponse

    @property
    def final_rules(self):
        rule_map = Map([
            Rule(rule.uri, endpoint=endpoint, methods=rule.methods)
            for endpoint, rule in self.adapted_rules.iteritems()
        ])
        return rule_map
