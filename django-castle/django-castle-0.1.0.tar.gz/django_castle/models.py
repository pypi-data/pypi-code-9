from django.contrib import auth
from api import Castle

__author__ = 'jens'

# Here we mainly define the signals to integrate into castle.io


def catch_login_signal(sender, request, user, **kwargs):
	castle = Castle()
	castle.log_login_success(user, request)

auth.signals.user_logged_in.connect(catch_login_signal, dispatch_uid="castle_login_signal")


def catch_logout_signal(sender, request, user, **kwargs):
	castle = Castle()
	castle.log_logout_success(user, request)

auth.signals.user_logged_out.connect(catch_logout_signal, dispatch_uid="castle_logout_signal")
