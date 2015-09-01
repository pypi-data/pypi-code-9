"""
composer.py
"""
from django import template
from django.conf import settings
from django.core.urlresolvers import reverse

from ..models import Element


register = template.Library()


class LazyContent:
    """
    Wrapper around a `NodeList` that is lazily-evaluated to a string.
    """
    def __init__(self, nodelist, context):
        self.nodelist = nodelist
        self.context = context

    def __str__(self):
        return self.nodelist.render(self.context)


def serialize_context(context):
    """
    Serializes a dictionary, list, or object into an easy to read example of the
    context.
    """
    if type(context) == dict:
        return '\n'.join(['%s = %r' % (key, val) for key, val in context.items()])

    if type(context) == list:
        result = 'list of %d elements' % len(context)
        for i, e in enumerate(context[0:15]):
            result += '\n%2d = %r' % (i, e)
        if len(context) > 15:
            result += '\n ...\n%2d = %r' % (len(context), context[-1])
        return result

    if context is not None or context != {}:
        result = 'object: ' + repr(context)

    return ''


class ComposerNode(template.Node):

    def __init__(self, name, content=None, nodelist=None, context_var=None, dynamic=False):
        self.name = name
        self.content = content
        self.nodelist = nodelist
        self.dynamic = dynamic
        if context_var is not None:
            self.context_var = template.Variable(context_var)
        else:
            self.context_var = None

    def render(self, context):
        """
        The `template_name` context variable must be present.
        """
        if self.nodelist:
            self.content = LazyContent(self.nodelist, context)

        template = context.get('template_name', None)
        elements = context.get('composer_elements', None)
        if template is None or elements is None:
            return str(self.content)

        has_perm = context.get('can_compose_permission', False)

        el_context = {}
        if self.context_var is not None:
            el_context = self.context_var.resolve(context)

        if self.name not in elements:
            context['composer_elements'][self.name] = Element.objects.create(
                template_name=template,
                name=self.name,
                is_dynamic=self.dynamic,
                context_example=serialize_context(el_context),
                content=str(self.content))

        element = elements[self.name]
        try:
            result = element.render(self.content, el_context)
        except Exception as e:
            if has_perm:
                result = str(e)
            else:
                result = element.content

        if has_perm:
            url = reverse('composer-edit-element', kwargs={'pk': element.id})
            result = '<div class="edit-composer-button">edit</div>' + result
            result = '<div class="edit-composer-element" data-url="%s" data-name="%s">%s</div>' % (
                url, self.name, result)

        return result


def strip_quotes(val):
    quotes = ("'", '"')
    if type(val) == str and val[0] in quotes and val[-1] in quotes:
        return val[1:-1]
    return val


@register.tag(name='composer_dynamic')
def do_composer_dynamic(parser, token):
    """
    This tag expects the following format:

        {% composer_dynamic 'name' context_var %}
            This is the default template, which can use {% if blah %}context {{vars}}{% endif %}
        {% endcomposer %}

    The second argument is optional.
    """
    bits = token.split_contents()
    name, context_var = None, None
    try:
        if len(bits) == 2:
            _, name = bits
        else:
            _, name, context_var = bits
    except ValueError:
        raise template.TemplateSyntaxError(
            '%r tag requires either 1 or 2 arguments' % token.contents.split()[0])

    name = strip_quotes(name)
    nodelist = parser.parse(('endcomposer',))
    parser.delete_first_token()
    return ComposerNode(name, nodelist=nodelist, context_var=context_var, dynamic=True)


@register.tag(name='composer_static')
def do_composer_static(parser, token):
    """
    This tag expects the following format:

        {% composer_static 'name' %}Some static default content.{% endcomposer %}
    """
    try:
        _, name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            '%r tag requires exactly 1 argument' % token.contents.split()[0])

    name = strip_quotes(name)
    nodelist = parser.parse(('endcomposer',))
    parser.delete_first_token()
    return ComposerNode(name, nodelist=nodelist)


@register.simple_tag(takes_context=True)
def composer_includes(context):
    """
    Include the composer JS and CSS files in a page if the user has permission.
    """
    if context.get('can_compose_permission', False):
        url = settings.STATIC_URL
        url += '' if url[-1] == '/' else '/'
        js = '<script type="text/javascript" src="%sjs/composer.min.js"></script>' % url
        css = '<link rel="stylesheet" type="text/css" href="%scss/composer.css">' % url
        return js + css
    return ''
