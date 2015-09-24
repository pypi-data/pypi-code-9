import json
from okapi.templatetags.exports.base import export


def escape_payload(s):
    return json.dumps(s.replace('\n', ''))


def export_curl(request):
    template_name = 'exports/curl.html'
    return export(request, template_name)
