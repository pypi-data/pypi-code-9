from django import forms
from django.utils.translation import ugettext_lazy as _


class ProfileForm(forms.Form):
    """
    Form to update one's profile.
    """
    first_name = forms.CharField(required=True, label=_("First name"))
    last_name = forms.CharField(required=True, label=_("Last name"))
    email = forms.EmailField(required=True, label=_("E-mail"))
    telephone = forms.CharField(required=True, label=_("Telephone"))
