# -*- coding: utf-8 -*-

__author__ = 'marcos.medeiros'

from django.conf.urls import include, url
from django.contrib.auth.models import User

from rapid.registry import Action
from rapid.models import Application, Profile
from rapid.forms import ManageUsers

import rapid
from rapid import permissions

def _can_manage_users(request):
    if not request.user.is_authenticated:
        return None
    return request.user.application.managed_applications.profile_set

urlpatterns = rapid.register_model(Application, 'aplicacao',
                             write_set=permissions.to_admin(Application), read_set=permissions.to_all(Application)) +\
    rapid.register_model(Profile, write_set=permissions.to_admins(Profile), read_set=permissions.to_staff(Profile)) +\
    rapid.register_instance_form(Profile, 'manage_users', u'Gerenciar Usuários',
                            ManageUsers, _can_manage_users, "fa-users",
                            Action.Visibility.list) +\
    rapid.register_simple_select(User, ['username'], permissions.to_staff(User), 'usuario')

