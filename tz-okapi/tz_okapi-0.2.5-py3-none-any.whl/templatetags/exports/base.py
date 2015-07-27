
def export(request, template_name):
    """
    :param request: Request instance
    :type request: okapi.core.request.Request

    :return: Rendered export
    :rtype: str
    """
    from okapi.settings import settings
    template = settings.template.env.get_template(template_name)
    return template.render(request=request)
