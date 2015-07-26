from unittest import TestCase
from ids import IDS
from workitem import Workitem


class TestIDS(TestCase):
    @classmethod
    def setUpClass(self):
        self.ids = IDS("https://hub.jazz.net/ccm10", "", "")

    def test_create_session(self):
        assert self.ids.session is not None

    def test_get_work_item_by_id(self):
        WI = self.ids.get_work_item_by_id(16219)
        assert WI is not None
        assert isinstance(WI, Workitem)
        assert WI.id == "16219"
        assert WI.url is not None
        assert WI.description is not None
        print WI.url

    def test_get_work_item_by_owner(self):
        WI = self.ids.get_work_items_by_owner("James Royal")
        assert WI is not None
        assert isinstance(WI, list)
        WI = WI[0]
        assert WI.id == "16219"
        assert WI.url is not None
        assert WI.description is not None


