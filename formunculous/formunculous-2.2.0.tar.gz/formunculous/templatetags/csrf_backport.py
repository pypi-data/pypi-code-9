from django import template


# This is just to make formunculous works in any Django version 1.1 and up.
# it is registered in the __init__ for formunculous if we are using a version
# that doesn't have this tag.

register = template.Library()

class CsrfTokenNode(template.Node):
    # This no-op tag exists to allow 1.1.X code to be compatible with Django 1.2
    def render(self, context):
        return u''

def csrf_token(parser, token):

    return CsrfTokenNode()

register.tag(csrf_token)
