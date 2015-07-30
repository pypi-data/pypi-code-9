from okta.framework.ApiClient import ApiClient
from okta.framework.Utils import Utils
from okta.models.usergroup.UserGroup import UserGroup


class UserGroupsClient(ApiClient):
    def __init__(self, base_url, api_token):
        ApiClient.__init__(self, base_url + '/api/v1/groups', api_token)

    # CRUD
    def get_groups(self, limit=None, query=None, after=None, filter_string=None, url=None):
        if url:
            response = ApiClient.get(self, url)
            return Utils.deserialize(response.text, UserGroup)

        params = {
            'limit': limit,
            'query': query,
            'after': after,
            'filter': filter_string
        }
        response = ApiClient.get_path(self, '/', params=params)
        return Utils.deserialize(response.text, UserGroup)

    def get_group(self, gid):
        response = ApiClient.get_path(self, '/{0}'.format(gid))
        return Utils.deserialize(response.text, UserGroup)

    def update_group(self, group):
        return self.update_group_by_id(group.id, group)

    def update_group_by_id(self, gid, group):
        response = ApiClient.put_path(self, '/{0}'.format(gid), group)
        return Utils.deserialize(response.text, UserGroup)

    def create_group(self, group):
        response = ApiClient.post_path(self, '/', group)
        return Utils.deserialize(response.text, UserGroup)

    def delete_group(self, gid):
        response = ApiClient.delete_path(self, '/{0}'.format(gid))
        return Utils.deserialize(response.text, UserGroup)