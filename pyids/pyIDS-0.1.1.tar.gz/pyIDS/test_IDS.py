from unittest import TestCase
from ids import IDS
from workitem import Workitem


class TestIDS(TestCase):
    @classmethod
    def setUpClass(self):
        self.ids = IDS("https://hub.jazz.net/ccm10", "user", "pass")

    def test_create_session(self):
        assert self.ids.session is not None

    def test_get_work_item(self):
        WI = self.ids.get_work_item("16219")
        assert WI is not None
        assert isinstance(WI, Workitem)

        assert WI.id is not None
        assert WI.url is not None
        assert WI.description is not None
        print WI.tags
        print WI.priority
        print WI.creation_date
        print WI.due_date


