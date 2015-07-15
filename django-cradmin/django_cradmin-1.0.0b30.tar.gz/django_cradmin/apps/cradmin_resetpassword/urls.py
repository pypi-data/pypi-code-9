from __future__ import unicode_literals
from django.conf.urls import url, patterns
from django_cradmin.apps.cradmin_resetpassword.views.begin import BeginPasswordResetView
from django_cradmin.apps.cradmin_resetpassword.views.email_sent import EmailSentView
from django_cradmin.apps.cradmin_resetpassword.views.reset import ResetPasswordView

urlpatterns = patterns(
    '',
    url(r'^begin',
        BeginPasswordResetView.as_view(),
        name="cradmin-resetpassword-begin"),
    url(r'^email-sent',
        EmailSentView.as_view(),
        name="cradmin-resetpassword-email-sent"),
    url(r'^reset/(?P<token>.+)',
        ResetPasswordView.as_view(),
        name="cradmin-resetpassword-reset"),
)
