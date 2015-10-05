from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import CustomAuthTokenSerializer

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import HttpResponse
from django.contrib.auth import logout

import json
import pytz
import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

BAD_REQUEST_SIGNUP = "User can not be created!"

class CustomAuthTokenView(ObtainAuthToken):

    def post(self, request):
        serializer = CustomAuthTokenSerializer(data=request.data)

        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer._validated_data['user'])

            utc_now = pytz.utc.localize(datetime.datetime.utcnow())
            token_lifetime = token.created + datetime.timedelta(hours=settings.EXPIRATION_TIME)
            if not created and (token_lifetime < utc_now):
                token.delete()
                token = Token.objects.create(user=serializer._validated_data['user'])
                token.created = utc_now
                token.save()

            response_data = {'token': token.key}
            return Response(response_data, content_type='application/json', status=status.HTTP_200_OK)

        else:
            return Response(dict(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

def sign_up(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')

    if not username:
        username = email

    user = User(username=username, email=email, password=password)
    try:
        user.full_clean()
        user.save()
        return HttpResponse(json.dumps({'token': user._auth_token_cache.key}), status=status.HTTP_201_CREATED, content_type='application/json')
    except:
        return HttpResponse(json.dumps({'error': BAD_REQUEST_SIGNUP}), status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

class LogoutAuthTokenView(APIView):

    def post(self, request):
        try:
            token = request._auth
            token = Token.objects.get(key=token)
            token.delete()
        except Token.DoesNotExist:
            pass
        return HttpResponse(json.dumps({'detail': 'success'}), status=status.HTTP_200_OK, content_type='application/json')
