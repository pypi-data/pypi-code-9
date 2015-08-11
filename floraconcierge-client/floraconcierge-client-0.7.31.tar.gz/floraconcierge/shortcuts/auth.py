from floraconcierge.shortcuts import get_apiclient


def exists(email, app_id):
    return get_apiclient().services.auth.exists(email, app_id)


def set_result(token_id, is_success, data):
    return get_apiclient().services.auth.set_result(token_id, is_success, data)


def get_token(id):
    return get_apiclient().services.auth.get_token(id)
