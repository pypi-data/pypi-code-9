from django import forms

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
