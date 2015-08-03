__author__ = 'admin'
from webmocker.mock_helper import pretender_defaults


class Request:

  def __init__(self):
    self.url = pretender_defaults.url
    self.headers = {}
    self.body = pretender_defaults.request_body
    self.method = pretender_defaults.method


  def set_request_entities(self,request_json):
    from webmocker.mock_helper import pretend_helpers
    self.url = pretend_helpers.get_url_from_json(request_json)                                                    # get the URL from the json
    self.method = request_json['method'] if 'method' in request_json else pretender_defaults.method         # get the request method from the json
    self.body = pretend_helpers.get_body_from_json(request_json)                                                  # get the request body from the json
    self.headers = pretend_helpers.get_headers_from_json(request_json)                                            # get the request headers from the json