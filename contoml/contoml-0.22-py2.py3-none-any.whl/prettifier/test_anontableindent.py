import contoml
from contoml.prettifier import anontableindent


def test_anon_table_indent():
    toml_text = """
    key=value
          another_key =44
noname = me
"""

    expected_toml_text = """
key=value
another_key =44
noname = me
"""

    f = contoml.loads(toml_text)
    f.prettify(prettifiers=[anontableindent.anon_table_indent])
    assert expected_toml_text == f.dumps()
