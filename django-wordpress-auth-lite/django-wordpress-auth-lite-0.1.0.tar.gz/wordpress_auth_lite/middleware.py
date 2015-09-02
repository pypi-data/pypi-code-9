from django.utils.functional import SimpleLazyObject

from wordpress_auth_lite.utils import get_wordpress_user


class WordPressAuthMiddleware(object):
    def process_request(self, request):
        request.wordpress_user = SimpleLazyObject(lambda: get_wordpress_user(request))
