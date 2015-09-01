"""
admin.py
"""
from django.contrib import admin
from django.contrib import messages

from .models import Element


class ComposerElementAdmin(admin.ModelAdmin):
    """
    Admin for the composer elements.
    """
    fields = ('content', 'context_example')
    readonly_fields = (
        'template_name', 'name', 'is_dynamic', 'has_changed', 'last_changed', 'changed_by')
    list_display = ('template_name', 'name', 'has_changed', 'last_changed', 'changed_by')
    list_filter = ('is_dynamic', 'has_changed')

    def save_model(self, request, obj, form, change):
        """
        Attempt to save the model.
        """
        try:
            obj.attempt_update(form.cleaned_data['content'], request.user)
        except Exception as e:
            messages.error(request, 'Could not update element, %s' % str(e))


admin.site.register(Element, ComposerElementAdmin)
