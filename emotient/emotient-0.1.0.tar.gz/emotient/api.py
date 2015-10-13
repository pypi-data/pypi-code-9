from collections import namedtuple

import emotient
import emotient.http_client
from emotient.managers import GroupManager, MediaManager
from emotient.resources import GroupResource, MediaResource


APIInfo = namedtuple('APIInfo', ['key', 'http_client', 'base', 'version'])


class EmotientAnalyticsAPI(object):

    def __init__(self, api_key, http_client=None, api_base=None, api_version=None):
        self.api_key = api_key

        if api_base is not None:
            self.api_base = api_base
        else:
            self.api_base = emotient.api_base

        if http_client is not None:
            self.http_client = http_client
        else:
            self.http_client = emotient.http_client.get_http_client()

        if api_version is not None:
            self.api_version = api_version
        else:
            self.api_version = emotient.api_version

        api_info = APIInfo(self.api_key, self.http_client, self.api_base, self.api_version)
        self.groups = GroupManager(api_info, GroupResource)
        self.media = MediaManager(api_info, MediaResource)

    def __repr__(self):
        return u'{}: {}'.format(type(self).__name__, self.api_base)
