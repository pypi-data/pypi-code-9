from okapi.templatetags import headers
from okapi.templatetags.exports import curl, jira
from okapi.templatetags import misc


filters = {
    'nl2br': misc.nl2br,
    'status_code_class': misc.status_code_class,

    'escape_payload': curl.escape_payload,
    'headers_as_string': headers.headers_as_string,

    'export_curl': curl.export_curl,
    'export_jira': jira.export_plain,
}
