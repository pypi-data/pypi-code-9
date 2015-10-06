from incuna_test_utils.testcases.api_request import BaseAPIRequestTestCase

from model_logging.serializers import LogEntrySerializer
from . import factories
from .utils import get_log_entry_data


class TestLogEntrySerializer(BaseAPIRequestTestCase):
    user_factory = factories.UserFactory

    @classmethod
    def setUpTestData(cls):
        cls.user = factories.UserFactory.create()
        cls.entry = factories.LogEntryFactory.create(user=cls.user, creator=cls.user)

    def setUp(self):
        self.context = {'request': self.create_request(user=self.user)}

    def test_serialize(self):
        serializer = LogEntrySerializer(instance=self.entry, context=self.context)
        expected = get_log_entry_data(self.entry)
        self.assertEqual(serializer.data, expected)

    def test_serialize_data_json(self):
        """Ensure `data` is decoded as `json`."""
        serializer = LogEntrySerializer(instance=self.entry, context=self.context)
        self.assertIsInstance(serializer.data['data'], dict)
