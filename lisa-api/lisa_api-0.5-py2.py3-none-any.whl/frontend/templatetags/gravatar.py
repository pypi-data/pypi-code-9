"""
### gravatar.py ###############
### place inside a 'templatetags' directory inside the top level of a Django app (not project, must be inside an app)
### at the top of your page template include this:
### {% load gravatar %}
### and to use the url do this:
### <img src="{% gravatar_url 'someone@somewhere.com' %}">
### or
### <img src="{% gravatar_url sometemplatevariable %}">
### just make sure to update the "default" image path below
"""

from django import template
from six.moves.urllib.parse import urlencode
import hashlib

register = template.Library()


class GravatarUrlNode(template.Node):
    def __init__(self, email):
        self.email = template.Variable(email)

    def render(self, context):
        try:
            email = self.email.resolve(context)
            if not email:
                email = ''
        except template.VariableDoesNotExist:
            return ''

        default = 'mm'
        size = 40

        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower().encode('utf-8')).hexdigest() + "?"
        gravatar_url += urlencode({'d': default, 's': str(size)})

        return gravatar_url


@register.tag
def gravatar_url(parser, token):
    try:
        tag_name, email = token.split_contents()

    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])

    return GravatarUrlNode(email)
