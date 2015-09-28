from threading import local

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils import translation
from django.utils.cache import patch_vary_headers


PARAMETER_NAME = 'language_code'
COOKIE_NAME = 'language_code'


def _get_localization_local():
    result = local()
    result.LANGUAGE_CODE = 'iv-IV'
    result.LANGUAGE_ID = 0

    return result

thread_local = _get_localization_local()


class LocalizationMiddleware(object):
    @staticmethod
    def get_language_id(default=0):
        global thread_local

        if hasattr(thread_local, 'LANGUAGE_ID'):
            return thread_local.LANGUAGE_ID
        else:
            return default

    @staticmethod
    def get_language_code(default=''):
        global thread_local

        if hasattr(thread_local, 'LANGUAGE_CODE'):
            return thread_local.LANGUAGE_CODE
        else:
            return default

    def process_request(self, request):
        global thread_local

        language_code = settings.LANGUAGE_CODE

        if PARAMETER_NAME in request.GET:
            language_code = request.GET[PARAMETER_NAME]
        elif COOKIE_NAME in request.COOKIES:
            language_code = request.COOKIES[COOKIE_NAME]
        else:
            language_code = settings.LANGUAGE_CODE

        from localization.models import Language

        try:
            language = Language.objects.get(code__iexact=language_code)
        except Language.DoesNotExist:
            raise ImproperlyConfigured("Unsupported language code.")

        translation.activate(language.code)

        request.LANGUAGE_CODE = translation.get_language()
        request.LANGUAGE_ID = language.id
        thread_local.LANGUAGE_CODE = request.LANGUAGE_CODE
        thread_local.LANGUAGE_ID = request.LANGUAGE_ID

    def process_response(self, request, response):
        language_code = translation.get_language()

        if hasattr(response, 'set_cookie'):
            response.set_cookie(COOKIE_NAME, language_code, max_age=31536000)
            patch_vary_headers(response, ('Accept-Language',))

            if not 'Content-Language' in response:
                response['Content-Language'] = language_code

        del thread_local.LANGUAGE_CODE
        del thread_local.LANGUAGE_ID

        return response
