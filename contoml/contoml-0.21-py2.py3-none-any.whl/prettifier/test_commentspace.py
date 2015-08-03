import contoml
from contoml.prettifier import commentspace


def test_comment_space():

    toml_text = """
my_key = string
id = 12 # My special ID

[section.name]
headerk = false
# Own-line comment should stay the same
other_key = "value"
"""

    expected_toml_text = """
my_key = string
id = 12\t# My special ID

[section.name]
headerk = false
# Own-line comment should stay the same
other_key = "value"
"""

    f = contoml.loads(toml_text)
    f.prettify(prettifiers=[commentspace.comment_space])
    assert expected_toml_text == f.dumps()
