"""
from django.conf.urls import patterns, url, include
from django.contrib.auth.views import password_change
from django.views.generic import TemplateView

from django.contrib.auth import views as auth_views

from .views import *
from .forms import PasswordResetForm

urlpatterns = patterns('',
    # -- Account Management Functions
    # url(r'^account/register/$', CreateAccount.as_view(),
    #     name='registration_register'),
    # url(r'^account/update/$', UpdateAccount.as_view(), name='account_update'),
    # url(r'^account/password/change/$', AccountUpdatePassword.as_view(),
    #     name='account_update_password'),


    url(r'^login/$', LoginRegisterView.as_view(), name="login_and_register"),
    url(r'^account/$', AccountDashboardView.as_view(), name="account_dashboard"),

    # -- Account Management Functions
    url(r'^account/update/$', AccountUpdate.as_view(), name='account_update'),
    url(r'^account/update/done/$', AccountUpdateDone.as_view(), name='account_update_done'),
    url(r'^account/password/change/$', AccountUpdatePassword.as_view(), name='account_update_password'),

    # -- Password Override URL's
    url(r'^account/password/reset/$',
                auth_views.password_reset,
               {'password_reset_form': PasswordResetForm}, name='password_reset',),

    url(r'^account/password/reset/done/$',
                auth_views.password_reset_done,
                name='password_reset_done'),
    url(r'^account/password/reset/complete/$',
                auth_views.password_reset_complete,
                name='password_reset_complete'),
    url(r'^account/password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
                auth_views.password_reset_confirm,
                name='password_reset_confirm'),    


    url(r'^account/register/$', CreateAccount.as_view(), name='create_account'),
    url(r'^account/login/$', redirect_login_view, name='login'),


    
    

    # -- Account/Registration URL's
    (r'^account/logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}),

    (r'^account/', include('registration.backends.default.urls')),

    url(r'^admin/dashboard_stats/account/user/$', BaseUserDashboardStatsView.as_view(), name='dashboard_stats_account_user'),
)"""