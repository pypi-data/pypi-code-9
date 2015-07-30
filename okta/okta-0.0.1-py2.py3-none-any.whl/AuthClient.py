from okta.framework.ApiClient import ApiClient
from okta.framework.Utils import Utils
from okta.models.auth.AuthResult import AuthResult


class AuthClient(ApiClient):
    def __init__(self, base_url, api_token):
        ApiClient.__init__(self, base_url + '/api/v1/authn', api_token)

    def authenticate(self, username, password,
                     relay_state=None, response_type=None, force_mfa=None, context=None):
        request = {
            'username': username,
            'password': password,
            'relayState': relay_state,
            'context': context
        }

        params = {
            'forceMfa': force_mfa,
            'responseType': response_type
        }

        response = ApiClient.post_path(self, '/', request, params=params)
        return Utils.deserialize(response.text, AuthResult)

    def auth_with_factor(self, state_token, factor_id, pass_code,
                         relay_state=None, remember_device=None):
        request = {
            'stateToken': state_token,
            'passCode': pass_code,
            'relayState': relay_state
        }

        params = {
            'rememberDevice': remember_device
        }

        response = ApiClient.post_path(self, '/factors/{0}/verify'.format(factor_id),
                                      request, params=params)
        return Utils.deserialize(response.text, AuthResult)

    # MFA MANAGEMENT

    def enroll_factor(self, state_token, factor_type, provider, profile, relay_state=None):
        request = {
            'stateToken': state_token,
            'factorType': factor_type,
            'provider': provider,
            'profile': profile,
            'relayState': relay_state
        }

        response = ApiClient.post_path(self, '/factors', request)
        return Utils.deserialize(response.text, AuthResult)

    def activate_factor(self, state_token, factor_id, passcode, relay_state=None):
        request = {
            'stateToken': state_token,
            'passCode': passcode,
            'relayState': relay_state
        }

        response = ApiClient.post_path(self, '/factors/{0}/lifecycle/activate'.format(factor_id), request)
        return Utils.deserialize(response.text, AuthResult)

    def resend_code(self, state_token, factor_id, relay_state=None):
        request = {
            'stateToken': state_token,
            'relayState': relay_state
        }

        response = ApiClient.post_path(self, '/factors/{0}/lifecycle/resend'.format(factor_id), request)
        return Utils.deserialize(response.text, AuthResult)

    # CREDENTIAL MANAGEMENT

    def change_password(self, state_token, old_password, new_password, relay_state=None):
        request = {
            'stateToken': state_token,
            'oldPassword': old_password,
            'newPassword': new_password,
            'relayState': relay_state
        }

        response = ApiClient.post_path(self, '/credentials/change_password', request)
        return Utils.deserialize(response.text, AuthResult)

    def reset_password(self, state_token, old_password, new_password, relay_state=None):
        request = {
            'stateToken': state_token,
            'newPassword': new_password,
            'relayState': relay_state
        }

        response = ApiClient.post_path(self, '/credentials/reset_password', request)
        return Utils.deserialize(response.text, AuthResult)

    def forgot_password(self, username, relay_state=None):
        request = {
            'username': username,
            'relayState': relay_state
        }

        response = ApiClient.post_path(self, '/recovery/password', request)
        return Utils.deserialize(response.text, AuthResult)

    def forgot_password_answer(self, state_token, security_answer, new_password, relay_state=None):
        request = {
            'stateToken': state_token,
            'securityAnswer': security_answer,
            'newPassword': new_password,
            'relayState': relay_state
        }

        response = ApiClient.post_path(self, '/recovery/answer', request)
        return Utils.deserialize(response.text, AuthResult)

    # RECOVERY

    def validate_recovery_token(self, recovery_token, relay_state=None):
        request = {
            'recoveryToken': recovery_token,
            'relayState': relay_state
        }

        response = ApiClient.post_path(self, '/recovery/token', request)
        return Utils.deserialize(response.text, AuthResult)

    def unlock_account(self, username, relay_state=None):
        request = {
            'username': username,
            'relayState': relay_state
        }

        response = ApiClient.post_path(self, '/recovery/unlock', request)
        return Utils.deserialize(response.text, AuthResult)

    def unlock_account_answer(self, state_token, security_answer, relay_state=None):
        request = {
            'stateToken': state_token,
            'securityAnswer': security_answer,
            'relayState': relay_state
        }

        response = ApiClient.post_path(self, '/recovery/answer', request)
        return Utils.deserialize(response.text, AuthResult)

    # STATE MANAGEMENT

    def previous_state(self, state_token, relay_state=None):
        request = {
            'stateToken': state_token,
            'relayState': relay_state
        }

        response = ApiClient.post_path(self, '/previous', request)
        return Utils.deserialize(response.text, AuthResult)

    def get_status(self, state_token, relay_state=None):
        request = {
            'stateToken': state_token,
            'relayState': relay_state
        }

        response = ApiClient.post_path(self, '/', request)
        return Utils.deserialize(response.text, AuthResult)

    def verify_transaction(self, factor_id, transaction_id, user_response):
        request = {
            'result': user_response
        }

        response = ApiClient.post_path(self, '/factors/{0}/transactions/{1}/verify'.format(factor_id, transaction_id), request)
        return Utils.deserialize(response.text, AuthResult)