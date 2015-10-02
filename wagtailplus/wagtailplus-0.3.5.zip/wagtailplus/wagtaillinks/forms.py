"""
Contains application form definitions.
"""
from django import forms

from wagtailplus.wagtaillinks.models import Link


class EmailLinkForm(forms.models.ModelForm):
    """
    Form for email link instances.
    """
    class Meta(object):
        model   = Link
        fields  = ('link_type', 'title', 'email', 'tags')
        widgets = {
            'link_type': forms.HiddenInput,
        }

    def __init__(self, *args, **kwargs):
        """
        Sets initial value for link type.
        """
        super(EmailLinkForm, self).__init__(*args, **kwargs)
        self.fields['link_type'].initial    = Link.LINK_TYPE_EMAIL
        self.fields['email'].required       = True

class ExternalLinkForm(forms.models.ModelForm):
    """
    Form for external link instances.
    """
    class Meta(object):
        model   = Link
        fields  = ('link_type', 'title', 'external_url', 'tags')
        widgets = {
            'link_type': forms.HiddenInput,
        }

    def __init__(self, *args, **kwargs):
        """
        Sets initial value for link type.
        """
        super(ExternalLinkForm, self).__init__(*args, **kwargs)
        self.fields['link_type'].initial        = Link.LINK_TYPE_EXTERNAL
        self.fields['external_url'].required    = True
