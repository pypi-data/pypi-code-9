# -*- coding: utf-8 -*-

__author__ = 'marcos.medeiros'

from django.conf.urls import include, url
from django.contrib.auth.models import User

from rapid.registry import Action
from rapid.models import Application, Profile
from rapid.forms import ManageUsers

from rapid import views
from rapid import permissions

def _can_manage_users(request):
    if not request.user.is_authenticated:
        return []
    return request.user.application.managed_applications.profile_set

_manage_users_permistion = permissions.Permission(
    lambda r: False,
    _can_manage_users
)

urlpatterns = views.register_model(Application, 'aplicacao',
                             write_set=permissions.to_superusers(), read_set=permissions.to_all()) +\
    views.register_model(Profile, write_set=permissions.to_superusers(), read_set=permissions.to_staff()) +\
    views.register_instance_form(Profile, 'manage_users', u'Gerenciar Usuários',
                            ManageUsers, _manage_users_permistion, "fa-users",
                            Action.Visibility.list) +\
    views.register_simple_select(User, ['username'], permissions.to_staff(), 'usuario')

