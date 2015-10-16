from pygments.lexer import RegexLexer, bygroups, include
from pygments.token import Name, Operator, Punctuation, Number, Text, String

__all__ = ['BabeltraceLexer']


class BabeltraceLexer(RegexLexer):
    name = 'Babeltrace'
    aliases = ["babeltrace"]
    filenames = ["*.lttng"]

    tokens = {
        'root': [
            (r'{', Punctuation, 'keyval'),
            (r'\(', Punctuation, 'diff'),
            (r'\[', Punctuation, 'time'),
            (r'(\w+)(:)(\w+):', bygroups(Name.Function, Punctuation, Name.Tag)),
            (r'(\S)+', Name.Tag),
            include('punctuation'),
            include('blank')
        ],
        'diff': [
            (r'[0-9\?]+', Name.Variable),
            (r'\+', Operator),
            (r'\)', Punctuation, '#pop'),
            include('punctuation'),
            include('blank')
        ],
        'time': [
            (r'\w+', String),
            (r'\]', Punctuation, '#pop'),
            include('punctuation'),
        ],
        'keyval': [
            (r'(\w+)(\s=\s)(0x)([0-9A-Fa-f]+)', bygroups(Name.Attribute, Operator, Number.Hex, Number.Hex)),
            (r'(\w+)(\s=\s)(")([^"]*)(")', bygroups(Name.Attribute, Operator, Punctuation, String, Punctuation)),
            (r'(\w+)(\s=\s)(\d+\.\d+)', bygroups(Name.Attribute, Operator, Number.Float)),
            (r'(\w+)(\s=\s)(\d+)', bygroups(Name.Attribute, Operator, Number.Integer)),
            (r'}', Punctuation, '#pop'),
            (r'(\w+)(\s=\s)(\[)', bygroups(Name.Attribute, Operator, Punctuation), 'sequence'),
            include('punctuation'),
            include('blank')
        ],
        'sequence': [
            (r'(\[)(\d+)(\])(\s=\s)(\d+)', bygroups(Punctuation, Name.Constant, Punctuation, Operator, Number.Integer)),
            (r'(\[)(\d+)(\])(\s=\s)(0x)([0-9A-Fa-fx]+)', bygroups(Punctuation, Name.Constant, Punctuation, Operator, Number.Hex, Number.Hex)),
            (r'\s(\])', Punctuation, '#pop'),
            include('punctuation'),
            include('blank')
        ],
        'punctuation': [
            (r'[.:,+]', Punctuation)
        ],
        'blank': [
            (r'[\s]', Text.Whitespace)
        ]
    }
