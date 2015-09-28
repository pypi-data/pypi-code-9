from django import template

from html import escape
from urllib.parse import parse_qsl
from urllib.parse import urlencode
from urllib.parse import urlsplit
from urllib.parse import urlunsplit


register = template.Library()


class UrlParamsNode(template.Node):
    def __init__(self, reset, parameters):
        self.reset = reset
        self.parameters = parameters

    def render(self, context):
        if self.reset:
            query_data = []
        else:
            try:
                url_data = urlsplit(context['request'].get_full_path())
                query_data = parse_qsl(url_data.query, keep_blank_values=True)
            except:
                query_data = []

        query_dict = dict(query_data)

        for name, value in self.parameters.items():
            if isinstance(name, str):
                param_name = name
            else:
                try:
                    param_name = name.resolve(context)
                except template.VariableDoesNotExist:
                    param_name = str(name)

            if isinstance(value, str):
                param_value = value
            else:
                try:
                    param_value = value.resolve(context)
                except template.VariableDoesNotExist:
                    param_value = str(value)

            query_dict[param_name] = param_value

        return escape(urlunsplit(('', '', '', urlencode( [(key, query_dict[key]) for key in query_dict] ), '')))


@register.tag(name='url_params')
def url_params(parser, token):
    def add_parameter(parser, dictionary, name, value):
        if (name[0] == '"') and (name[-1] == '"'):
            name = name[1:-1]
        elif (name[0] == '\'') and (name[-1] == '\''):
            name = name[1:-1]
        else:
            name = parser.compile_filter(name)

        if (value[0] == '"') and (value[-1] == '"'):
            value = value[1:-1]
        elif (value[0] == '\'') and (value[-1] == '\''):
            value = value[1:-1]
        else:
            value = parser.compile_filter(value)

        dictionary[name] = value

    contents = token.split_contents()
    tag_name = contents.pop(0)

    if len(contents) == 0:
        raise template.TemplateSyntaxError("{0} tag requires at least one argument.".format(tag_name))

    if contents[0] in ['/', '?']:
        reset = True
        contents = contents[1:]
    else:
        reset = False

    parameters = {}
    pair_name = None

    for item in contents:
        if pair_name:
            add_parameter(parser, parameters, pair_name, item)
            pair_name = None
        else:
            pair = item.split('=', 1)

            if len(pair) == 1:
                pair_name = item
            else:
                add_parameter(parser, parameters, pair[0], pair[1])

    if pair_name:
        add_parameter(parser, parameters, pair_name, '""')

    return UrlParamsNode(reset, parameters)
