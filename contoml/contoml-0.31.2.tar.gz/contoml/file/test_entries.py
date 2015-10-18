from contoml import parser, lexer
from contoml.file import toplevels
from contoml.parser.tokenstream import TokenStream


def test_entry_extraction():
    text = open('sample.toml').read()
    elements = parser.parse_token_stream(TokenStream(lexer.tokenize(text)))

    e = tuple(toplevels.identify(elements))

    assert len(e) == 13
    assert isinstance(e[0], toplevels.AnonymousTable)


def test_entry_names():
    name_a = toplevels.Name(('super', 'sub1'))
    name_b = toplevels.Name(('super', 'sub1', 'sub2', 'sub3'))

    assert name_b.is_prefixed_with(name_a)
    assert name_b.without_prefix(name_a).sub_names == ('sub2', 'sub3')
