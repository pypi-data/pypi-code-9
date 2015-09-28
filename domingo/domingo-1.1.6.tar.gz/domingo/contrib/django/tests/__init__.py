from unittest import TestCase
from domingo.fields import AbstractSet
from domingo.contrib.django.fields import DjangoFKList


class DjangoContribTests(TestCase):

    def test_DjangoFKList_is_a_set_field(self):
        self.assertTrue(issubclass(DjangoFKList, AbstractSet))
