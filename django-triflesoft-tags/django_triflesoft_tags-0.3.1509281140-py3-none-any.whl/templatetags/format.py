from django import template


register = template.Library()


class FormatNode(template.Node):
    def __init__(self, parameters):
        self.parameters = []

        for parameter in parameters:
            if (parameter[0] == '"') and (parameter[-1] == '"'):
                self.parameters.append(parameter[1:-1])
            elif (parameter[0] == '\'') and (parameter[-1] == '\''):
                self.parameters.append(parameter[1:-1])
            else:
                self.parameters.append(template.Variable(parameter))

    def render(self, context):
        values = []

        for parameter in self.parameters:
            if isinstance(parameter, str):
                values.append(parameter)
            else:
                try:
                    values.append(parameter.resolve(context))
                except template.VariableDoesNotExist:
                    values.append(parameter)

        return str(values[0]).format(*values[1:])


@register.tag(name='format')
def format(parser, token):
    contents = token.split_contents()
    tag_name = contents.pop(0)
    parameters = contents

    if len(parameters) == 0:
        raise template.TemplateSyntaxError("{0} tag requires at least one argument.".format(tag_name))

    return FormatNode(parameters)
