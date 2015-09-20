from django.contrib import admin

from .models import Condition, Chain, ChainElement


admin.site.register(Condition)
admin.site.register(Chain)
admin.site.register(ChainElement)
