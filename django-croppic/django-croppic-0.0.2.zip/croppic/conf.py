from django.conf import settings

min_size_error = 'Image is too small, must be at least {0}x{1} wide.'

USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
UPLOAD_TO = getattr(settings, 'CROPPIC_UPLOAD_PATH', 'pictures')
MIN_SIZE = getattr(settings, 'CROPPIC_MIN_SIZE', None)  # tuple (width, height) e.g. CROPPIC_MIN_SIZE = (250, 250)
MIN_SIZE_ERROR = getattr(settings, 'CROPPIC_MIN_SIZE_ERROR', min_size_error)
if MIN_SIZE:
    MIN_SIZE_ERROR = MIN_SIZE_ERROR.format(*MIN_SIZE)
