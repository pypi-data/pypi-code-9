
import pytest
from ..portfolio import Portfolio, nav_menu


def test___():
    class A(Portfolio):
        pass

    a = A()
    a.__(name="PYLOT", live=True)

    assert a._context.get("name") == "PYLOT"
    assert a._context.get("live") is True

def test_extends__():

    class A(Portfolio):
        name = "A"

    class AA(Portfolio):
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
            self.__(WHO="WHO")
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

def test__meta():
    class A(Portfolio):
        def __init__(self):
            self.page_meta(title="TITLE")
            self.page_meta(description="DESCRIPTION")

        def get_meta(self, k):
            return self._context.get(Portfolio.PAGE_META)[k]
    a = A()

    assert a.get_meta("title") == "TITLE"
    assert a.get_meta("description") == "DESCRIPTION"


def test_nav_menu():

    #@nav_menu("Home", order=1)
    class Home(Portfolio):

        @nav_menu("Welcome")
        def index(self):
            pass

    Portfolio.init(__name__)

    nav_menu = Portfolio._context["NAV_MENU"]

    assert len(nav_menu) == 1
