import json
from copy import copy

from django.http import HttpResponse
from django.utils.encoding import force_text

from restify.http import status


class PostInBodyMiddleware(object):
    def _is_json_body_request(self, request):
        return request.POST.dict() == {} and\
               len(request.body) and\
               request.META['CONTENT_TYPE'] == 'application/json'


    def process_request(self, request):
        if not self._is_json_body_request(request):
            return

        try:
            body = json.loads(force_text(request.body))

            # Update request post
            post = copy(request.POST)
            post.update(body)
            request.POST = body
        except ValueError:
            resp = HttpResponse()
            resp.status_code = status.HTTP_400_BAD_REQUEST
            return resp