# coding: utf-8
from ..base import Resource


class SyncResource(Resource):
    __slots__ = ('token', 'resource_point')
    resource_point = None

    def __init__(self, token=None, *args, **kwargs):
        self.token = token
        super(SyncResource, self).__init__(*args, **kwargs)

    def get_headers(self):
        headers = super(SyncResource, self).get_headers()
        if self.token:
            headers['Authorization'] = 'Token {}'.format(self.token)
        return headers

    def get(self, slug, *args, **kwargs):
        return self.request(method='GET', url=self.get_entrypoint(*tuple(self.resource_point + (slug,))), *args, **kwargs)

    def put(self, slug, *args, **kwargs):
        return self.request(method='PUT', url=self.get_entrypoint(*tuple(self.resource_point + (slug,))), *args, **kwargs)

    def patch(self, slug, *args, **kwargs):
        return self.request(method='PATCH', url=self.get_entrypoint(*tuple(self.resource_point + (slug,))), *args, **kwargs)
