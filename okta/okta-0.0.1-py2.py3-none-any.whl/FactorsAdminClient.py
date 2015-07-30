from okta.framework.ApiClient import ApiClient
from okta.framework.Utils import Utils
from okta.models.factor.OrgAuthFactor import OrgAuthFactor


class FactorsAdminClient(ApiClient):

    def __init__(self, base_url, api_token):
        ApiClient.__init__(self, base_url + '/api/v1/org', api_token)

    def get_org_factors(self, filter=None):
        params = {
            'filter': str(filter)
        }
        response = ApiClient.get_path(self, '/factors', params=params)
        return Utils.deserialize(response.text, OrgAuthFactor)

    def activate_org_factor(self, org_factor_id, org_auth_factor=None):
        response = ApiClient.post_path(self, '/factors/{0}/lifecycle/activate'.format(org_factor_id), org_auth_factor)
        return Utils.deserialize(response.text, OrgAuthFactor)

    def deactivate_org_factor(self, org_factor_id):
        response = ApiClient.post_path(self, '/factors/{0}/lifecycle/deactivate'.format(org_factor_id))
        return Utils.deserialize(response.text, OrgAuthFactor)