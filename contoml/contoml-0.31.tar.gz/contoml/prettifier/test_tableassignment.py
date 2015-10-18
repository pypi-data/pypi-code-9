
import contoml
from .tableassignment import table_assignment_spacing


def test_table_assignment_spacing():
    toml_text = """
    key1= "my value"
    key2 =42
    keys        =   [4, 5,1]

    [section]
    key1= "my value"
    key2 =42
    keys        =   [4, 5,1]
"""

    expected_prettified = """
    key1 = "my value"
    key2 = 42
    keys = [4, 5,1]

    [section]
    key1 = "my value"
    key2 = 42
    keys = [4, 5,1]
"""

    f = contoml.loads(toml_text)
    f.prettify(prettifiers=[table_assignment_spacing])
    assert expected_prettified == f.dumps()
