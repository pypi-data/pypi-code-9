from django import forms
from django.utils.translation import ugettext_lazy as _


class AnonymousRegistrationForm(forms.Form):
    """
    Form to register
    """
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
