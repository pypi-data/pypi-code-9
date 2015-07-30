from okta.framework.ApiClient import ApiClient
from okta.framework.Utils import Utils
from okta.models.factor.FactorCatalogEntry import FactorCatalogEntry
from okta.models.factor.Factor import Factor
from okta.models.factor.Question import Question
from okta.models.factor.FactorVerificationResponse import FactorVerificationResponse
from okta.models.factor.FactorDevice import FactorDevice


class FactorsClient(ApiClient):

    def __init__(self, base_url, api_token):
        ApiClient.__init__(self, base_url + '/api/v1/users', api_token)

    def get_factors_catalog(self, user_id):
        response = ApiClient.get_path(self, '/{0}/factors/catalog'.format(user_id))
        return Utils.deserialize(response.text, FactorCatalogEntry)

    def get_lifecycle_factors(self, user_id):
        response = ApiClient.get_path(self, '/{0}/factors'.format(user_id))
        return Utils.deserialize(response.text, Factor)

    # FACTOR CRUD

    def get_available_questions(self, user_id):
        response = ApiClient.get_path(self, '/{0}/factors/questions'.format(user_id))
        return Utils.deserialize(response.text, Question)

    def enroll_factor(self, user_id, factor_enroll_request, update_phone=None):
        params = {
            'updatePhone': update_phone
        }
        response = ApiClient.post_path(self, '/{0}/factors'.format(user_id), factor_enroll_request, params=params)
        return Utils.deserialize(response.text, Factor)

    def get_factor(self, user_id, user_factor_id):
        response = ApiClient.get_path(self, '/{0}/factors/{1}'.format(user_id, user_factor_id))
        return Utils.deserialize(response.text, Factor)

    def update_factor(self, user_id, user_factor_id, factor_enroll_request):
        response = ApiClient.put_path(self, '/{0}/factors/{1}'.format(user_id, user_factor_id), factor_enroll_request)
        return Utils.deserialize(response.text, Factor)

    def reset_factor(self, user_id, user_factor_id):
        ApiClient.delete_path(self, '/{0}/factors/{1}'.format(user_id, user_factor_id))

    # FACTOR LIFECYCLE

    def activate_factor(self, user_id, factor_id, passcode, next_passcode=None):
        request = {
            'passCode': passcode,
            'next_passcode': next_passcode
        }
        response = ApiClient.post_path(self, '/{0}/factors/{1}/lifecycle/activate'.format(user_id, factor_id), request)
        return Utils.deserialize(response.text, Factor)

    def resend_code(self, user_id, user_factor_id):
        response = ApiClient.post_path(self, '/{0}/factors/{1}/resend'.format(user_id, user_factor_id))
        return Utils.deserialize(response.text, Factor)

    def verify_factor(self, user_id, factor_id, activation_token=None, answer=None, passcode=None, next_passcode=None):
        request = {
            'activationToken': activation_token,
            'answer': answer,
            'passCode': passcode,
            'nextPassCode': next_passcode
        }
        response = ApiClient.post_path(self, '/{0}/factors/{1}/verify'.format(user_id, user_factor_id), request)
        return Utils.deserialize(response.text, FactorVerificationResponse)

    # FACTOR DEVICE CRUD

    def enroll_factor_device(self, user_id, factor_enroll_request):
        response = ApiClient.post_path(self, '/{0}/devices'.format(user_id), factor_enroll_request)
        return Utils.deserialize(response.text, FactorDevice)

    def get_factor_device(self, user_id, user_factor_id, device_id):
        response = ApiClient.get_path(self, '/{0}/factors/{1}/device/{2}'.format(user_id, user_factor_id, device_id))
        return Utils.deserialize(response.text, FactorDevice)

    def update_factor_device(self, user_id, factor_device_request):
        response = ApiClient.post_path(self, '/{0}/factors/{1}'.format(user_id), factor_device_request)
        return Utils.deserialize(response.text, FactorDevice)

    # FACTOR DEVICE LIFECYCLE

    def activate_factor_device(self, user_id, user_factor_id, device_id, passcode):
        request = {
            'passCode': passcode
        }
        response = ApiClient.post_path(self, '/{0}/factors/{1}/devices/{2}/lifecycle/activate'.format(
            user_id, user_factor_id, device_id), request)
        return Utils.deserialize(response.text, Factor)