from floraconcierge.shortcuts import get_apiclient


def exists(email, app_id):
    return get_apiclient().services.auth.exists(email, app_id)


def login(app_id, email, password=None, remember=None, checkip=None):
    return get_apiclient().services.auth.login(
        app_id,
        email,
        password=password,
        remember=remember,
        checkip=checkip)


def reset_password(email, app_id):
    return get_apiclient().services.auth.reset_password(email, app_id)


def set_result(token_id, is_success, data):
    return get_apiclient().services.auth.set_result(token_id, is_success, data)


def get_token(id):
    return get_apiclient().services.auth.get_token(id)
