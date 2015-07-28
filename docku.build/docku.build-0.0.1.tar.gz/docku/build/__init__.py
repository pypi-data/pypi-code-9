import json
import os

class BuildConfig(dict):
    def __init__(self, path):
        cc = {}
        with open(path) as fh:
            cc = json.load(fh)
        super().__init__(cc)
        self.populate_envvars()

    def populate_envvars(self):
        keys = ['BINTRAY_TOKEN', 'BINTRAY_USER', 'BINTRAY_REPO']
        for key in keys:
            value = os.getenv(key)
            if value:
                self[key] = value
