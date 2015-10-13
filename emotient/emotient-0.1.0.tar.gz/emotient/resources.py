from emotient.emotient_client import APIWrapper
from emotient.managers import GroupMediaManager
from emotient.mixins import (ListMixin, CreateMixin, InstanceRetrieveMixin, InstanceUpdateMixin, InstanceDeleteMixin,
                             InstanceAnalyticsMixin, InstanceAggregatedAnalyticsMixin, InstanceMetadataCSVMixin,)
from emotient.models import Group, GroupMedia, Media
from emotient.utils import parse_dts


class EmotientObject(object):
    model = None

    def __init__(self, api_info, data):
        self._api = api_info
        self._client = APIWrapper(api_info.key, api_info.http_client, api_info.base, api_info.version)
        self.data = data
        self.id = data['id']
        parse_dts(self.data)

    def __repr__(self):
        return u'{}: {}'.format(type(self).__name__, self.id)

    def to_instance(self, resp):
        if isinstance(resp, list):
            return [self.to_instance(i) for i in resp]
        elif isinstance(resp, dict):
            self.__init__(self._api, resp)
            return self
        else:
            return resp


class MediaResource(EmotientObject, ListMixin, InstanceRetrieveMixin, InstanceUpdateMixin, InstanceDeleteMixin,
                    InstanceAnalyticsMixin, InstanceAggregatedAnalyticsMixin):
    model = Media


class GroupResource(EmotientObject, ListMixin, CreateMixin, InstanceRetrieveMixin, InstanceUpdateMixin,
                    InstanceDeleteMixin, InstanceAggregatedAnalyticsMixin, InstanceMetadataCSVMixin):
    model = Group

    def __init__(self, *args, **kwargs):
        super(GroupResource, self).__init__(*args, **kwargs)

        stimulus = self.data['stimulus']
        if stimulus is not None:
            self.data['stimulus'] = MediaResource(self._api, stimulus)

        self.media = GroupMediaManager(self.id, self._api, MediaResource)


class GroupMediaResource(MediaResource):
    model = GroupMedia
