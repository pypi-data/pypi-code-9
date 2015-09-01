
import pytest
from bluebook import Bluebook


def test_set_context__():
    class A(Bluebook):
        pass

    a = A()
    a.set_context__(name="PYLOT", live=True)

    assert a._context.get("name") == "PYLOT"
    assert a._context.get("live") is True

def test_extends__():

    class A(Bluebook):
        name = "A"

    class AA(Bluebook):
        v = "JJ"

    a = A()
    aa = AA()

    @a.extends__
    class B(object):
        CONST = "CONSTANT"
        def b(self):
            return "B"

    @a.extends__
    @aa.extends__  # Remember the order of the placement
    class C(object):
        def c(self):
            self.set_context__(WHO="WHO")
            return "C"

    @aa.extends__
    class D(object):
        def d(self):
            return "D"

    @a.extends__  # Extends a function
    def hello(self):
        return "HELLO"

    # Assert A
    assert a.b() == "B"
    assert a.c() == "C"
    assert a.hello() == "HELLO"
    assert a.CONST == "CONSTANT"
    assert a._context.get("WHO") == "WHO"

    # Assert AA
    assert aa.c() == "C"
    assert aa.d() == "D"

    # Exceptions
    with pytest.raises(AttributeError):
        # @aa didn't get attached to B, because it was called before @a was extended
        assert aa.CONST == "CONSTANT"
        assert aa.hello() == "HELLO"

def test_set_meta__():
    class A(Bluebook):
        def __init__(self):
            self.set_meta__(title="TITLE")
            self.set_meta__(description="DESCRIPTION")

        def get_meta(self, k):
            return self._context.get("META")[k]
    a = A()

    assert a.get_meta("title") == "TITLE"
    assert a.get_meta("description") == "DESCRIPTION"


