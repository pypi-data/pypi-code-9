import unittest2
from mock import Mock, patch
from applause import settings
from applause.buaps import ApplauseBuilds


def open_patcher(func):
    if "__builtin__" in globals():
        return lambda func: patch("__builtin__.open")(func)
    else:
        # Python 3.x:
        return lambda func: patch("builtins.open")(func)


class ApplauseBuildsTest(unittest2.TestCase):
    __name__ = ""   # Hack to make open_patcher work

    def setUp(self):
        self.session_mock = Mock()
        self.buaps = ApplauseBuilds(self.session_mock)

    def test_get_upload_info_success(self):
        response_mock = Mock()
        response_mock.json.return_value = {"some": "json"}
        self.session_mock.post.return_value = response_mock
        info = self.buaps.get_upload_info("process", {"basic": {"some": "input"}}, "file_name")
        assert info == {"some": "json"}
        self.session_mock.post.assert_called_once_with(settings.BUAPS_STORE_URL, data={
            "action": "process", "workflows": '{"basic": {"some": "input"}}',
            "original_name": "file_name", "redirect": "none",
        })
        response_mock.raise_for_status.assert_called_once_with()

    def test_get_upload_status_success(self):
        response_mock = Mock()
        response_mock.json.return_value = {"status": "dict"}
        self.session_mock.get.return_value = response_mock
        status = self.buaps.get_upload_status("abc123")
        assert status == {"status": "dict"}
        self.session_mock.get.assert_called_once_with(settings.BUAPS_BASE_URL + "storage/abc123/status/")
        response_mock.raise_for_status.assert_called_once_with()

    @open_patcher
    @patch("applause.buaps.requests")
    def test_upload_file(self, requests_mock, open_mock):
        open_mock.return_value = "fileobj"
        response_mock = Mock()
        requests_mock.post.return_value = response_mock
        self.buaps.upload_file("url", "some data", "and path")
        requests_mock.post.assert_called_once_with(url="url", files={"file": "fileobj"}, data="some data")
        self.assertTrue(response_mock.raise_for_status.called)

    @patch('applause.buaps.time.sleep', lambda seconds: None)
    def test_process_build(self):
        self.buaps.get_upload_info = Mock(return_value={
            "token": "abc123", "url": "url_to_store_file", "data": {"upload": "data"},
        })
        self.buaps.get_upload_status = Mock(return_value={'status': 'done'})
        self.buaps.upload_file = Mock()
        self.buaps.trigger_processing = Mock()

        token = self.buaps.process_build("a/path/to/somefile.xxx", {"input": "data"})
        assert token == "abc123"

        self.buaps.get_upload_info.assert_called_once_with(action="process", workflow={
            "basic": {"original_name": "somefile.xxx", "input": "data"}
        }, name="somefile.xxx")
        self.buaps.upload_file.assert_called_once_with(
            url="url_to_store_file", data={"upload": "data"}, path="a/path/to/somefile.xxx",
        )
        self.buaps.trigger_processing.assert_called_once_with("abc123")
        self.buaps.get_upload_status.assert_called_once_with("abc123")

    def test_trigger_processing(self):
        response_mock = Mock()
        self.session_mock.get.return_value = response_mock
        self.buaps.trigger_processing("abc123")
        self.session_mock.get.assert_called_once_with(settings.BUAPS_BASE_URL + "handlers/success/abc123/")
        response_mock.raise_for_status.assert_called_once_with()
