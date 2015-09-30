from django.utils.html import escape
from codeschool.graders import errors
_print_func = print


def example_to_html(example):
    '''Render a parsed IO template into HTML'''

    out = []
    if isinstance(example, str):
        return escape(example)
    for x in example:
        data = x.replace('\n', '<br>')  # TODO: proper HTML escaping
        if x.is_input:
            data = '<span style="color: #f00;">&lt;%s&gt;</span>' % data
            data += '<br>'
        out.append(data)
    return ''.join(out)  # + '<pre>%s</pre>' % (example)


def message_bad_format(got, expected):
    got = '<strong>Valor obtido</strong><br>' + example_to_html(got)
    expected = '<strong>Resposta esperada</strong><br>' + \
        example_to_html(expected)
    return '<div>%s<br><br>%s</div>' % (got, expected)


def message_from_exception(ex):
    return str(type(ex).__name__ + ': ' + str(ex))
