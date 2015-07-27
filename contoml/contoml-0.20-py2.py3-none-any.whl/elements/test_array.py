import pytest
from contoml import lexer
from contoml.elements.array import ArrayElement
from contoml.elements.atomic import AtomicElement
from contoml.elements.metadata import PunctuationElement, WhitespaceElement, NewlineElement


def test_array_element():
    tokens = tuple(lexer.tokenize('[4, 8, [42, \n 23], 15]'))
    assert len(tokens) == 19
    sub_elements = (
        PunctuationElement(tokens[:1]),

        AtomicElement(tokens[1:2]),
        PunctuationElement(tokens[2:3]),
        WhitespaceElement(tokens[3:4]),

        AtomicElement(tokens[4:5]),
        PunctuationElement(tokens[5:6]),
        WhitespaceElement(tokens[6:7]),

        ArrayElement((
            PunctuationElement(tokens[7:8]),

            AtomicElement(tokens[8:9]),
            PunctuationElement(tokens[9:10]),
            WhitespaceElement(tokens[10:11]),
            NewlineElement(tokens[11:12]),
            WhitespaceElement(tokens[12:13]),

            AtomicElement(tokens[13:14]),
            PunctuationElement(tokens[14:15]),
        )),

        PunctuationElement(tokens[15:16]),
        WhitespaceElement(tokens[16:17]),
        AtomicElement(tokens[17:18]),
        PunctuationElement(tokens[18:19])
    )

    array_element = ArrayElement(sub_elements)

    # Test length
    assert len(array_element) == 4

    # Test getting a value
    assert array_element[0] == 4
    assert array_element[1] == 8
    assert array_element[2][0] == 42
    assert array_element[2][1] == 23
    assert array_element[-1] == 15

    # Test assignment with a negative index
    array_element[-1] = 12

    # Test persistence of formatting
    assert '[4, 8, [42, \n 23], 12]' == array_element.serialized()

    # Test raises IndexError on invalid index
    with pytest.raises(IndexError) as _:
        print(array_element[5])

    # Test appending a new value
    array_element[2].append(77)
    assert '[4, 8, [42, \n 23, 77], 12]' == array_element.serialized()

    # Test deleting a value
    del array_element[2][1]
    assert '[4, 8, [42, 77], 12]' == array_element.serialized()

    # Test primitive_value
    assert [4, 8, [42, 77], 12] == array_element.primitive_value
