from django.contrib import admin

from djangocms_contact.models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'email', 'subject', 'creation_date', 'message')
    fields = ('name', 'email', 'subject', 'creation_date', 'message')
    list_display = ('subject', 'name', 'email', 'creation_date')
