import contoml
from contoml.elements import traversal as t, factory as element_factory
from contoml.prettifier import linelength


def test_splitting_string():
    toml_text = """
k = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In et lectus nec erat condimentum scelerisque gravida sed ipsum. Mauris non orci tincidunt, viverra enim eget, tincidunt orci. Sed placerat nibh vitae ante maximus egestas maximus eu quam. Praesent vehicula mauris vestibulum, mattis turpis sollicitudin, aliquam felis. Pellentesque volutpat pharetra purus vel finibus. Vestibulum sed tempus dui. Maecenas auctor sit amet diam et porta. Morbi id libero at elit ultricies porta vel vitae nullam. "
"""

    expected_toml_text = """
k = \"\"\"
Lorem ipsum dolor sit amet, consectetur adipiscing elit. In et lectus nec erat condimentum scelerisque gravida sed \\
ipsum. Mauris non orci tincidunt, viverra enim eget, tincidunt orci. Sed placerat nibh vitae ante maximus egestas \\
maximus eu quam. Praesent vehicula mauris vestibulum, mattis turpis sollicitudin, aliquam felis. Pellentesque volutpat \\
pharetra purus vel finibus. Vestibulum sed tempus dui. Maecenas auctor sit amet diam et porta. Morbi id libero at elit \\
ultricies porta vel vitae nullam. \"\"\"
"""
    f = contoml.loads(toml_text)
    f.prettify(prettifiers=[linelength.line_lingth_limiter])

    assert expected_toml_text == f.dumps()


def test_splitting_inline_table():
    toml_text = """

somethingweird = false

[section]
k = {a=1, b=2, c = 3, d = 4, e = 5, f = 6, g = 7, h = 8, i = 9, j = 10, k = 11, l = 12, m = 13, n = 14, o = 15, p = 16, q = 17}


[data]
id = 12

"""

    f = contoml.loads(toml_text)
    pre_prettified_primitive = f.primitive
    f.prettify(prettifiers=[linelength.line_lingth_limiter])

    assert f.primitive == pre_prettified_primitive
    assert all(len(line) < 120 for line in f.dumps().split('\n'))


def test_splitting_array():
    toml_text = """

somethingweird = false

[section]
k = [4, 8, 15, 16, 23, 42, 4, 8, 15, 16, 23, 42, 4, 8, 15, 16, 23, 42, 4, 8, 15, 16, 23, 42, 4, 8, 15, 16, 23, 42, 4, 8, 15, 16, 23, 42, 4, 8, 15, 16, 23, 42]


[data]
id = 12

"""

    f = contoml.loads(toml_text)
    pre_prettified_primitive = f.primitive
    f.prettify(prettifiers=[linelength.line_lingth_limiter])
    f.prettify(prettifiers=[linelength.line_lingth_limiter])

    assert f.primitive == pre_prettified_primitive
    assert all(len(line) < 120 for line in f.dumps().split('\n'))
