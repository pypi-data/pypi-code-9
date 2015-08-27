from django import forms
from django.conf import settings

from optionsfield.fields import OptionsWidget


class SectionAdminFormBase(forms.ModelForm):

    template_name = forms.TypedChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        super(SectionAdminFormBase, self).__init__(*args, **kwargs)
        choices = ((None, '------'), ) + self._meta.model.TEMPLATE_NAME_CHOICES
        self.fields['template_name'].choices = choices
        try:
            self.fields['options'].widget = OptionsWidget()
        except KeyError:
            pass

        if 'tinymce' in settings.INSTALLED_APPS:
            from tinymce.widgets import TinyMCE
            try:
                self.fields['description'].widget = \
                    TinyMCE(attrs={'cols': 80, 'rows': 30})
            except KeyError:
                pass
