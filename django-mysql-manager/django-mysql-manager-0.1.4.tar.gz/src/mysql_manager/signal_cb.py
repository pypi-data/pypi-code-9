# -*- coding: utf-8 -*-
#
#  This file is part of django-mysql-manager.
#
#  django-mysql-manager is a Django based management interface for MySQL users and databases.
#
#  Development Web Site:
#    - http://www.codetrax.org/projects/django-mysql-manager
#  Public Source Code Repository:
#    - https://source.codetrax.org/hgroot/django-mysql-manager
#
#  Copyright 2011 George Notaras <gnot [at] g-loaded.eu>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

try:
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    from django.db.models.loading import cache
    get_model = cache.get_model


def drop_user(sender, **kwargs):
    MySQLUser = get_model('mysql_manager', 'MySQLUser')
    instance = kwargs['instance']
    MySQLUser.objects.drop_user(instance.name)

    
def drop_database(sender, **kwargs):
    MySQLDatabase = get_model('mysql_manager', 'MySQLDatabase')
    instance = kwargs['instance']
    # First revoke the privileges of the user on this database
    MySQLDatabase.objects.revoke_privileges(instance.name, instance.user.name)
    # Then delete the database.
    MySQLDatabase.objects.drop_database(instance.name)

