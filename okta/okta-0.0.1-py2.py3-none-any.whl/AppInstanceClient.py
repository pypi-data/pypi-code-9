from okta.framework.ApiClient import ApiClient
from okta.framework.Utils import Utils
from okta.framework.PagedResults import PagedResults
from okta.models.app.AppInstance import AppInstance


class AppInstanceClient(ApiClient):
    def __init__(self, base_url, api_token):
        ApiClient.__init__(self, base_url + '/api/v1/apps', api_token)

    # CRUD

    def get_app_instances(self, limit=None, query=None, filter_string=None):
        params = {
            'limit': limit,
            'query': query,
            'filter': filter_string
        }
        response = ApiClient.get_path(self, '/', params=params)
        return Utils.deserialize(response.text, User)

    def get_paged_app_instances(self, limit=None, filter_string=None, after=None, url=None):
        if url:
            response = ApiClient.get(self, url)

        else:
            params = {
                'limit': limit,
                'after': after,
                'filter': filter_string
            }
            response = ApiClient.get_path(self, '/', params=params)

        return PagedResults(response, AppInstance)

    def create_app_instance(self, app_instance):
        response = ApiClient.post_path(self, '/', app_instance)
        return Utils.deserialize(response.text, AppInstance)

    def get_app_instance(self, id):
        response = ApiClient.get_path(self, '/' + str(id))
        return Utils.deserialize(response.text, AppInstance)

    def update_app_instance(self, id, app_instance):
        response = ApiClient.put_path(self, '/' + str(id), app_instance)
        return Utils.deserialize(response.text, AppInstance)

    def delete_app_instance(self, id):
        ApiClient.delete_path(self, '/' + str(id))

    # LIFECYCLE

    def activate_app_instance(self, id):
        ApiClient.post_path(self, '/' + id + '/lifecycle/activate', None)

    def deactivate_app_instance(self, id):
        ApiClient.post_path(self, '/' + id + '/lifecycle/deactivate', None)