from django import template

from molo.commenting.models import MoloComment

# NOTE: heavily inspired by
#       https://github.com/santiagobasulto/django-comments-utils


register = template.Library()


def get_molo_comments(parser, token):
    """
    Get a limited set of comments for a given object.
    Defaults to a limit of 5. Setting the limit to -1 disables limiting.

    usage:

        {% get_molo_comments for object as variable_name %}
        {% get_molo_comments for object as variable_name limit amount %}

    """
    keywords = token.contents.split()
    if len(keywords) != 5 and len(keywords) != 7:
        raise template.TemplateSyntaxError(
            "'%s' tag takes exactly 2 or 4 arguments" % (keywords[0],))
    if keywords[1] != 'for':
        raise template.TemplateSyntaxError(
            "first argument to '%s' tag must be 'for'" % (keywords[0],))
    if keywords[3] != 'as':
        raise template.TemplateSyntaxError(
            "first argument to '%s' tag must be 'as'" % (keywords[0],))
    if len(keywords) > 5 and keywords[5] != 'limit':
        raise template.TemplateSyntaxError(
            "third argument to '%s' tag must be 'limit'" % (keywords[0],))
    if len(keywords) > 5:
        return GetMoloCommentsNode(keywords[2], keywords[4], keywords[6])
    return GetMoloCommentsNode(keywords[2], keywords[4])


class GetMoloCommentsNode(template.Node):

    def __init__(self, obj, variable_name, limit=5):
        self.obj = obj
        self.variable_name = variable_name
        self.limit = int(limit)

    def render(self, context):
        try:
            obj = template.resolve_variable(self.obj, context)
        except template.VariableDoesNotExist:
            return ''

        qs = MoloComment.objects.for_model(obj.__class__).filter(
            object_pk=obj.pk)
        qs = qs.order_by("-submit_date")
        if self.limit > 0:
            qs = qs[:self.limit]
        context[self.variable_name] = list(qs)
        return ''

register.tag('get_molo_comments', get_molo_comments)
