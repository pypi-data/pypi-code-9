# coding=utf-8


def get_remote_addr(request):
    return request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])


def get_form_error_message(form):
    errors = form.errors
    result = []
    for k in errors:
        result.append(u'\r\n'.join(errors[k]))
    return u'\r\n'.join(result)
