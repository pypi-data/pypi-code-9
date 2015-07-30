from okta.framework.ApiClient import ApiClient
from okta.framework.Utils import Utils
from okta.framework.PagedResults import PagedResults
from okta.models.user.User import User
from okta.models.user.TempPassword import TempPassword


class UsersClient(ApiClient):
    def __init__(self, base_url, api_token):
        ApiClient.__init__(self, base_url + '/api/v1/users', api_token)

    # CRUD

    def get_users(self, limit=None, query=None, filter_string=None):
        params = {
            'limit': limit,
            'query': query,
            'filter': filter_string
        }
        response = ApiClient.get_path(self, '/', params=params)
        return Utils.deserialize(response.text, User)

    def get_user(self, uid):
        response = ApiClient.get_path(self, '/{0}'.format(uid))
        return Utils.deserialize(response.text, User)

    def update_user(self, user):
        return self.update_user_by_id(user.id, user)

    def update_user_by_id(self, uid, user):
        response = ApiClient.put_path(self, '/{0}'.format(uid), user)
        return Utils.deserialize(response.text, User)

    def create_user(self, user, activate=False):
        if activate is None:
            response = ApiClient.post_path(self, '/', user)
        else:
            params = {
                'activate': activate
            }
            response = ApiClient.post_path(self, '/', user, params=params)
        return Utils.deserialize(response.text, User)

    def delete_user(self, uid):
        response = ApiClient.delete_path(self, '/{0}'.format(uid))
        return Utils.deserialize(response.text, User)

    def get_paged_users(self, limit=None, filter_string=None, after=None, url=None):
        if url:
            response = ApiClient.get(self, url)

        else:
            params = {
                'limit': limit,
                'after': after,
                'filter': filter_string
            }
            response = ApiClient.get_path(self, '/', params=params)

        return PagedResults(response, User)

    # LIFECYCLE

    def deactivate_user(self, uid):
        response = ApiClient.post_path(self, '/{0}/lifecycle/deactivate'.format(uid))
        return Utils.deserialize(response.text, User)

    def unlock_user(self, uid):
        response = ApiClient.post_path(self, '/{0}/lifecycle/unlock'.format(uid))
        return Utils.deserialize(response.text, User)

    def expire_password(self, uid, temp_password=False):
        if not temp_password:
            ApiClient.post_path(self, '/{0}/lifecycle/expire_password'.format(uid))
        else:
            params = {
                'tempPassword': temp_password
            }
            response = ApiClient.post_path(self, '/{0}/lifecycle/expire_password'.format(uid), params=params)
            return Utils.deserialize(response.text, TempPassword)