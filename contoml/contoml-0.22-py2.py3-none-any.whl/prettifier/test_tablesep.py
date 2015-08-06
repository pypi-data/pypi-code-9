import contoml
from contoml.prettifier import tablesep


def test_table_separation():

    toml_text = """key1 = "value1"
key2 = 22
[section]
k = false
m= "true"



[another.section]
l = "t"
creativity = "on vacation"
"""

    expected_toml_text = """key1 = "value1"
key2 = 22

[section]
k = false
m= "true"

[another.section]
l = "t"
creativity = "on vacation"

"""

    f = contoml.loads(toml_text)
    f.prettify(prettifiers=[tablesep.table_separation])

    assert expected_toml_text == f.dumps()
