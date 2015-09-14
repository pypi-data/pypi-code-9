from django.conf.urls import url, patterns

urlpatterns = patterns(
    '',
    url(
        r'^password/reset/$',
        'django.contrib.auth.views.password_reset',
        {
            'post_reset_redirect': '/users/password/reset/done/',
            'template_name': 'registrations/password_reset_form.html'
        },
        name="password_reset"
    ),
    url(
        r'^password/reset/done/$',
        'django.contrib.auth.views.password_reset_done',
        {
            'template_name': 'registrations/password_reset_done.html'
        }
    ),
    url(
        r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {
            'post_reset_redirect': '/users/password/done/',
            'template_name': 'registrations/password_reset_confirm.html'
        },
        name="password_reset_confirm"
    ),
    url(
        r'^password/done/$',
        'django.contrib.auth.views.password_reset_complete',
        {
            'template_name': 'registrations/password_reset_complete.html'

        }
    ),
)
