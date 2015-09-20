from django.contrib import admin

from .models import Condition, Chain, ChainElement


class ChainElementInline(admin.TabularInline):
    model = ChainElement


class ChainAdmin(admin.ModelAdmin):
    inlines = (ChainElementInline,)


admin.site.register(Condition)
admin.site.register(Chain, ChainAdmin)
admin.site.register(ChainElement)
