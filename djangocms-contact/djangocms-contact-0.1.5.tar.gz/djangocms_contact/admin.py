from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from djangocms_contact.models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'email', 'subject', 'creation_date', 'message')
    fields = ('name', 'email', 'subject', 'creation_date', 'message')
    list_display = ('get_subject', 'name', 'email', 'creation_date')

    def get_subject(self, obj):
        if not obj.subject:
            return _('No subject')
        return obj.subject
    get_subject.short_description = _('Subject')
