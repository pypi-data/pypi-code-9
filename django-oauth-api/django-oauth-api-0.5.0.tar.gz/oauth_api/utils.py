from django.core.validators import URLValidator


def validate_uris(value):
    """
    Validate list of newline separated urls
    """
    v = URLValidator()
    for uri in value.split():
        v(uri)

def get_request_address(request):
    """
    Strips the actual request IP address from the X-FORWARDED-FOR header, if available.
    Otherwise non-proxied address is returned.
    """
    try:
        return request.META['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
    except KeyError:
        return request.META.get('REMOTE_ADDR', '0.0.0.0')