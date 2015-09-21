import requests


class FlarecastConfig(object):
    def __init__(self, config_url):
        self.config_url = config_url
        self.config = {}

        requests.packages.urllib3.disable_warnings()

    def load(self):
        config_resp = requests.get(self.config_url, verify=False)
        if config_resp.status_code != 200:
            print("Could not load global config file from %s" % self.config_url)
            exit(1)
        self.config = config_resp.json()

    def __getattr__(self, name):
        return self.config.get(name, None)
