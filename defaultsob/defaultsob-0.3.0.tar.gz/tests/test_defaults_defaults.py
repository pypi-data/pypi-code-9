import os
import sys
topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)
import unittest
from defaultsob import core


class Simple(core.Defaults):
    __slots__ = (
        "Name",
        "Description",
        "Additional"
    )
    Name = "Buzz"
    Description = core.use_name_if_none


class TestOrderedSet(unittest.TestCase):

    def test_ordered_set(self):
        self.assertEqual(
            core.ordered_set(
                [5, 5, 4, 4, 3, 3, 3]
            ), [5, 4, 3])


class TestClassSlots(unittest.TestCase):

    def test_class_slots(self):
        # self.assertEqual(expected, class_slots(ob))
        simple = Simple()
        slots = core.class_slots(simple)
        self.assertEqual(slots, ('Name', 'Description', 'Additional'))


class TestUseIfNone(unittest.TestCase):

    def test_use_if_none(self):
        simple = Simple()
        self.assertEqual(simple.Additional, None)
        value = core.usef('Name')('Additional', simple, {})
        self.assertEqual(value, "Buzz")


class TestChooseAlt(unittest.TestCase):

    def test_choose_alt(self):
        # self.assertEqual(expected, choose_alt(attr, ob, kwargs))
        simple = Simple()
        self.assertEqual(simple.Description, simple.Name)
        self.Description = None
        value = core.choose_alt("Description", simple, {})
        self.assertEqual(simple.Name, value)


class TestDefaults(unittest.TestCase):

    def test___init__(self):
        # core = Defaults(**kwargs)
        simple = Simple()
        self.assertEqual(simple.Name, 'Buzz')
        self.assertEqual(simple.Description, simple.Name)
        self.assertEqual(simple.Additional, None)
        simple = Simple(Description="Computer Blue")
        self.assertEqual(simple.Description, "Computer Blue")

    def test_to_dict(self):
        # core = Defaults(**kwargs)
        # self.assertEqual(expected, core.to_dict())
        simple = Simple(Additional="Bluebird", Description="Thunder")
        d = simple.to_dict()
        keys = sorted(d.keys())
        values = sorted(d.values())
        self.assertEqual(keys, ['Additional', 'Description', 'Name'])
        self.assertEqual(values, ['Bluebird', 'Buzz', 'Thunder'])
        d = Simple().to_dict_clean()
        keys = sorted(d.keys())
        self.assertEqual(keys, ['Description', 'Name'])

if __name__ == '__main__':
    unittest.main()
