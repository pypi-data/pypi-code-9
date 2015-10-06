# -*- coding: utf-8 -*-
'''
Copyright 2011-2015 ramusus
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes import generic

from facebook_api.admin import FacebookModelAdmin

from .models import User


class UserAdmin(FacebookModelAdmin):
    list_display = ('name','first_name','last_name','gender')
    list_display_links = ('name',)
    list_filter = ('gender',)
    search_fields = ('name',)

#    def get_readonly_fields(self, *args, **kwargs):
#        fields = super(UserAdmin, self).get_readonly_fields(*args, **kwargs)
#        return fields + ['likes']


if 'facebook_posts' in settings.INSTALLED_APPS:
    from facebook_posts.models import PostOwner, Comment

    class PostInline(generic.GenericTabularInline):
        model = PostOwner
        ct_field = 'owner_content_type'
        ct_fk_field = 'owner_id'
        fields = ('post',)
        readonly_fields = fields
        extra = False
        can_delete = False

    class CommentInline(generic.GenericTabularInline):
        model = Comment
        ct_field = 'author_content_type'
        ct_fk_field = 'author_id'
        fields = ('message','likes_count')
        readonly_fields = fields
        extra = False
        can_delete = False

    UserAdmin.inlines = [PostInline, CommentInline]

admin.site.register(User, UserAdmin)
