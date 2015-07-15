# -*- coding: utf-8 -*-
from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class I18NFormset(BaseInlineFormSet):
    """
    Generates an inline formset that is required
    """

    def __init__(self, *args, **kwargs):

        super(I18NFormset, self).__init__(*args, **kwargs)
        # self.forms[0].fields["language"].widget = TextInput(attrs={'readonly': 'readonly'})
        if len(self.forms) > 1:
            for i in range(1, len(self.forms)):
                self.forms[i].fields["language"].initial = self.forms[i].fields["language"].widget.choices[0][0]

    def _construct_form(self, i, **kwargs):
        """
        Override the method to change the form attribute empty_permitted
        """
        form = super(I18NFormset, self)._construct_form(i, **kwargs)

        if i == 0:
            form.empty_permitted = False
        return form


class ContentModelInLine(admin.StackedInline):
    max_num = len(settings.LANGUAGES)
    min_num = 1
    extra = 0
    formset = I18NFormset
    verbose_name = _("Content")
    verbose_name_plural = _("Contents")
    inline_classes = ('collapse open',)


class SynchronizedModelAdmin(admin.ModelAdmin):
    list_display = ('status', )
    list_filter = ('status', )
    readonly_fields = ('uuid', 'created', 'updated')
    exclude = ('deleted', )