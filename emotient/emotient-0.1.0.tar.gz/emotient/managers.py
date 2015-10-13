from emotient import models, utils
from emotient.emotient_client import APIWrapper
from emotient.error import EmotientAPIError
from emotient.mixins import (ListMixin, CreateMixin, RetrieveMixin, UpdateMixin, DeleteMixin, AnalyticsMixin,
                             AggregatedAnalyticsMixin, MetadataCSVMixin,)


class EmotientManager(object):
    model = None

    def __init__(self, api_info, resource_class):
        self._api = api_info
        self._client = APIWrapper(api_info.key, api_info.http_client, api_info.base, api_info.version)
        self.resource_class = resource_class

    def __repr__(self):
        return u'{}'.format(type(self).__name__)

    def to_instance(self, resp):
        if isinstance(resp, list):
            return [self.to_instance(i) for i in resp]
        elif isinstance(resp, dict):
            return self.resource_class(self._api, resp)
        else:
            raise EmotientAPIError(u'Invalid instance response')


class MediaManager(EmotientManager, ListMixin, RetrieveMixin, UpdateMixin, DeleteMixin, AnalyticsMixin,
                   AggregatedAnalyticsMixin):
    model = models.Media

    def upload(self, fp, timeout=80):
        files = {'file': fp}
        resp = self._client.request('POST', 'upload', files=files, timeout=timeout)
        new_media_id = resp['id']
        return self.retrieve(new_media_id)

    def search(self, query, sort=None, order='asc', page=1, per_page=50, timeout=10):
        params = {
            'q': query,
            'order': order,
            'page': page,
            'per_page': per_page
        }

        if sort is not None:
            params['sort'] = sort

        resp = self._client.request('GET', 'search', params=params, timeout=timeout)
        item_list = resp['items']
        return self.to_instance(item_list)


class GroupManager(EmotientManager, ListMixin, CreateMixin, RetrieveMixin, UpdateMixin, DeleteMixin,
                   AggregatedAnalyticsMixin, MetadataCSVMixin):
    model = models.Group


class GroupMediaManager(EmotientManager, ListMixin):

    def __init__(self, group_id, *args, **kwargs):
        super(GroupMediaManager, self).__init__(*args, **kwargs)
        self.model = type('GroupMedia', (models.Media,), dict(list_url=models.GroupMedia.list_url.format(group_id)))

    def add(self, media):
        """
        Add media to a group. Media can be a single ID, media instance, or list of IDs or media instances.
        """
        ids = utils.get_ids(media)
        return self._client.request('PUT', self.model.list_url, data={'ids': ids})

    def remove(self, media):
        """
        Remove media from a group. Media can be a single ID, media instance, or list of IDs or media instances.
        """
        ids = utils.get_ids(media)
        return self._client.request('DELETE', self.model.list_url, data={'ids': ids})
