from datetime import datetime
from email.utils import parsedate_to_datetime
from hashlib import md5
from hashlib import sha1
from hashlib import sha256
from hashlib import sha512
from hmac import new as new_hmac
from re import fullmatch

from django.contrib.auth import login
from django.http import HttpResponse

from token_auth.models import Token


class TokenAuthMiddleware(object):
    def __get_credentials(self, http_authorization):
        http_authorization_parts = http_authorization.split(' ')

        if len(http_authorization_parts) == 2:
            if http_authorization_parts[0].upper() == 'TOKEN':
                auth_token_code, auth_hmac = http_authorization_parts[1].split(':')

                return auth_token_code, auth_hmac

        return None, None

    def process_request(self, request):
        token_code = None
        auth_data = b''
        auth_hmac = ''

        if ('HTTP_AUTHORIZATION' in request.META) and ('HTTP_DATE' in request.META):
            now = datetime.utcnow()
            date_text = request.META['HTTP_DATE']
            date = parsedate_to_datetime(date_text)

            if abs(now.timestamp() - date.timestamp()) < 60:
                http_authorization = request.META['HTTP_AUTHORIZATION']
                token_code, auth_hmac = self.__get_credentials(http_authorization)
                auth_data = request.body + date_text.encode('ascii')
            else:
                return HttpResponse(
                    content='''Token authentication failure. Invalid Date header:
    Expected: {0:%Y-%m-%d %H:%M:%S} \u00B1 60 seconds
    Actual:   {1:%Y-%m-%d %H:%M:%S}.'''.format(now, date),
                    content_type='text/plain; charset=utf-8',
                    status=403)

        if (not token_code) or (not auth_data) or (not auth_hmac):
            return

        try:
            token = Token.objects.get(code=token_code, valid_from__lt=now, valid_till__gt=now)
        except Token.DoesNotExist:
            return HttpResponse(
                content='''Token authentication failure. Token does not exist or expired:
    Code: {0}.'''.format(token_code),
                content_type='text/plain; charset=utf-8',
                status=403)

        if not fullmatch(token.path_pattern, request.path):
            return HttpResponse(
                content='''Token authentication failure. Request path does not match token path:
    Expected: {0}
    Actual:   {1}.'''.format(token.path_pattern, request.path),
                content_type='text/plain; charset=utf-8',
                status=403)

        if not fullmatch(token.method_pattern, request.method):
            return HttpResponse(
                content='''Token authentication failure. Request method does not match token method:
    Expected: {0}
    Actual:   {1}.'''.format(token.path_pattern, request.path),
                content_type='text/plain; charset=utf-8',
                status=403)

        if token.can_md5 and (len(auth_hmac) == 32):
            data_hmac = new_hmac(bytes(token.secret), auth_data, md5).hexdigest()

            if sha512(data_hmac.lower().encode('ascii')).digest() != sha512(auth_hmac.lower().encode('ascii')).digest():
                return HttpResponse(
                    content='''Token authentication failure. MD5 HMAC mismatch.''',
                    content_type='text/plain; charset=utf-8',
                    status=403)
        elif token.can_sha1 and (len(auth_hmac) == 40):
            data_hmac = new_hmac(bytes(token.secret), auth_data, sha1).hexdigest()

            if sha512(data_hmac.lower().encode('ascii')).digest() != sha512(auth_hmac.lower().encode('ascii')).digest():
                return HttpResponse(
                    content='''Token authentication failure. SHA1 HMAC mismatch.''',
                    content_type='text/plain; charset=utf-8',
                    status=403)
        elif token.can_sha256 and (len(auth_hmac) == 64):
            data_hmac = new_hmac(bytes(token.secret), auth_data, sha256).hexdigest()

            if sha512(data_hmac.lower().encode('ascii')).digest() != sha512(auth_hmac.lower().encode('ascii')).digest():
                return HttpResponse(
                    content='''Token authentication failure. SHA256 HMAC mismatch.''',
                    content_type='text/plain; charset=utf-8',
                    status=403)
        elif token.can_sha512 and (len(auth_hmac) == 128):
            data_hmac = new_hmac(bytes(token.secret), auth_data, sha512).hexdigest()

            if sha512(data_hmac.lower().encode('ascii')).digest() != sha512(auth_hmac.lower().encode('ascii')).digest():
                return HttpResponse(
                    content='''Token authentication failure. SHA512 HMAC mismatch.''',
                    content_type='text/plain; charset=utf-8',
                    status=403)
        else:
            return HttpResponse(
                content='''Token authentication failure. HMAC type unknown.''',
                content_type='text/plain; charset=utf-8',
                status=403)

        user = token.user
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        request.user = user

        if hasattr(request, 'session'):
            login(request, user)
            request.session.flush()
