from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('amount', 'status', 'transaction_type', 
                    'content_object', 'created',)
    search_fields = ('secret', )


class TransactionInlineAdmin(GenericTabularInline):
    model = Transaction

    def has_add_permission(self, request):
        return False


admin.site.register(Transaction, TransactionAdmin)
