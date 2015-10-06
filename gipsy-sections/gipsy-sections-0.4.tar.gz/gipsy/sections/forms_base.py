from django import forms
from django.conf import settings

from optionsfield.fields import OptionsWidget


class SectionAdminFormBase(forms.ModelForm):

    template_name = forms.TypedChoiceField(
        required=False, label=u"Template",
        help_text=("Defines template type in which this object will be "
                   "rendered. Various templates have different look and "
                   "use different fields and options. Please refer to "
                   "documentation for details on template types."))

    def __init__(self, *args, **kwargs):
        super(SectionAdminFormBase, self).__init__(*args, **kwargs)
        choices = ((None, '------'), ) + self._meta.model.TEMPLATE_NAME_CHOICES
        self.fields['template_name'].choices = choices

        if 'title' in self.fields:
            self.fields['title'].help_text = "Name of a object - used in " \
                "templates as a <strong>headline</strong> or just for identification"

        if 'description' in self.fields:
            self.fields['description'].help_text = "<strong>copy,</strong> content of object"

        if 'options' in self.fields:
            self.fields['options'].widget = OptionsWidget()

        if 'tinymce' in settings.INSTALLED_APPS and 'description' in self.fields:
            from tinymce.widgets import TinyMCE
            self.fields['description'].widget = \
                TinyMCE(attrs={'cols': 80, 'rows': 30})


class SectionInlineAdminFormBase(SectionAdminFormBase):
    def __init__(self, *args, **kwargs):
        super(SectionInlineAdminFormBase, self).__init__(*args, **kwargs)
        # remove help text from inline formset as its too long and breaks look
        self.fields['template_name'].help_text = None
        self.fields['title'].help_text = None
