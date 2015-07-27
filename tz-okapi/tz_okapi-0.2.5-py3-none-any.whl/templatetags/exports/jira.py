from okapi.templatetags.exports.base import export


def export_plain(request):
    template_name = 'exports/jira.html'
    return export(request, template_name)
