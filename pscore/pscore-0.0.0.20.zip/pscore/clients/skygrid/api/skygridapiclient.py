from pscore.clients.skygrid.metadata.skygridmetadataclient import SkyGridMetaDataClient
from pscore.config.test_configuration import TestConfiguration as config
import requests
from ..dao.data import SGScreenShot, SGVideo
from datetime import datetime


class SkyGridApiClient(object):
    ACTION_SCREENSHOT = '/screenshot'
    ACTION_VIDEO_DIR = '/config'

    def __init__(self, driver):
        self.hub_url = config.get_hub_url()
        self.metadata_service_url = config.get_skygrid_service_url()
        self.metadata_client = SkyGridMetaDataClient(driver.test_context.logger)

        self.session_id = driver.session_id
        self.node_ip = driver.active_node_ip_no_port()
        self.video_output_directory = self.get_video_output_directory()

    def node_api_endpoint(self, action):
        return "{}:3000{}".format(self.node_ip, action)

    @staticmethod
    def _now():
        return str(datetime.now())

    def take_screenshot(self):
        url = self.node_api_endpoint(self.ACTION_SCREENSHOT)
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            path = data['file'][0]
            now = self._now()
            return SGScreenShot(self.session_id, path, now)
        else:
            return "Server responded with %s while trying to get screenshots" % response.status_code

    def get_video(self):
        path = "{}\\{}.mp4".format(self.video_output_directory, self.session_id)
        return SGVideo(self.session_id, path, self._now())

    def get_video_output_directory(self):

        config_url = self.node_api_endpoint(self.ACTION_VIDEO_DIR)
        response = requests.get(config_url)

        if response.status_code == 200:
            data = response.json()
            directory = data['config_runtime']['theConfigMap']['video_recording_options']['video_output_dir']
            return str(directory)
        else:
            return "Server responded with %s while trying to get videos" % response.status_code


