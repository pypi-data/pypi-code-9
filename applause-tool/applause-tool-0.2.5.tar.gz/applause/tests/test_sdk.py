from mock import Mock, patch
from requests import HTTPError
import unittest2
from applause.sdk import ApplauseSDK
from applause import settings


class ApplauseSDKTest(unittest2.TestCase):
    def setUp(self):
        self.session_mock = Mock()
        self.buaps_patcher = patch("applause.buaps.ApplauseBuilds")
        self.buaps_mock = self.buaps_patcher.start()
        self.sdk = ApplauseSDK(self.session_mock)

    def tearDown(self):
        self.buaps_patcher.stop()

    def test_upload(self):
        with patch('applause.product.ApplauseBuilds.process_build') as mock:
            self.sdk.upload_to_buaps(6, "path_to_file")
        mock.assert_called_once_with("path_to_file", {"app_id": 6})

    def test_create_installer_success(self):
        response_mock = Mock()
        response_mock.json.return_value = Mock(__getitem__=lambda self, key: 1122)
        self.session_mock.post.return_value = response_mock
        installer_id = self.sdk.create_installer("abc123", "changes")
        self.session_mock.post.assert_called_once_with(settings.SDK_INSTALLER_STORE_URL, data={
            "token": "abc123", "change_log": "changes", "is_current": True,
        })
        assert installer_id == 1122

    def test_create_installer_failure(self):
        self.session_mock.post.return_value = Mock(raise_for_status=Mock(side_effect=HTTPError))
        with self.assertRaises(HTTPError):
            self.sdk.create_installer("abc123", "changes")
        self.session_mock.post.assert_called_once_with(settings.SDK_INSTALLER_STORE_URL, data={
            "token": "abc123", "change_log": "changes", "is_current": True,
        })

    def test_distribute_success(self):
        self.sdk.upload_to_buaps = Mock()
        self.sdk.create_installer = Mock(return_value=33)

        self.sdk.distribute(11, 22, "/tmp/example.ipa", None, ["test1@example.com", "test2@example.com"])

        self.session_mock.post.assert_called_once_with(
            settings.SDK_BASE_URL + "companies/11/applications/22/distributions/",
            json={
                "installer": 33,
                "emails": ["test1@example.com", "test2@example.com"],
            },
        )

    def test_distribute_failure(self):
        self.sdk.upload_to_buaps = Mock()
        self.sdk.create_installer = Mock(return_value=33)
        self.session_mock.post.return_value = Mock(raise_for_status=Mock(side_effect=HTTPError))
        with self.assertRaises(HTTPError):
            self.sdk.distribute(11, 22, "/tmp/example.ipa", None, ["test1@example.com", "test2@example.com"])
        self.session_mock.post.assert_called_once_with(
            settings.SDK_BASE_URL + "companies/11/applications/22/distributions/",
            json={
                "installer": 33,
                "emails": ["test1@example.com", "test2@example.com"],
            },
        )

    @patch('applause.product.ApplauseBuilds.process_build')
    def test_distribute_no_emails(self, process_build_mock):
        self.sdk.create_installer = Mock()
        self.sdk.distribute(11, 22, "/tmp/example.ipa", None, [])
        self.assertFalse(self.session_mock.post.called)
