__author__ = 'hramik'
from django.contrib import admin
# from sorl.thumbnail.admin import AdminImageMixin
from djangocodemirror.fields import CodeMirrorWidget

from da_login.models import *


class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    extra = 0


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Relation)
admin.site.register(RelationType)
