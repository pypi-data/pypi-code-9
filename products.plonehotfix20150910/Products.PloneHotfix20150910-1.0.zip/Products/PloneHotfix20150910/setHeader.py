import inspect
from ZPublisher import HTTPResponse


def setHeader(self, name, value, literal=0, scrubbed=False):
    """ Set an HTTP return header on the response.

    Replay any existing value set for the header.

    If the 'literal' flag is true, preserve the case of the header name;
    otherwise the header name will be lowercased.

    'scrubbed' is for internal use, to indicate that another API has
    already removed any CRLF from the name and value.
    """
    if not scrubbed:
        name, value = HTTPResponse._scrubHeader(name, value)
    key = name.lower()
    name = literal and name or key
    self.headers[name] = value

source = inspect.getsource(HTTPResponse.HTTPResponse.setHeader)
if "The following is crazy" in source:
    HTTPResponse.HTTPResponse.setHeader = setHeader
