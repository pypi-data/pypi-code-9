# -*- coding: utf-8 -*-
from django.contrib import admin
import models
from django.utils.translation import ugettext_lazy as _

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "user", "content_type", "object_id"]
    list_filter  = ["user", "content_type"]
admin.site.register(models.Favorite, FavoriteAdmin)
