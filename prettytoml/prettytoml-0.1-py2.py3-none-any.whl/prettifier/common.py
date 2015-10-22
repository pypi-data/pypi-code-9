

def text_to_elements(toml_text):
    from ..lexer import tokenize
    from ..parser import parse_tokens
    return parse_tokens(tokenize(toml_text))


def elements_to_text(toml_elements):
    return ''.join(e.serialized() for e in toml_elements)


def assert_prettifier_works(source_text, expected_text, prettifier_func):
    assert expected_text == elements_to_text(prettifier_func(text_to_elements(source_text)))
