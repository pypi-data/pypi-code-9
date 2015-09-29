# -*- coding:utf-8 -*-
import re
from custom_auth.user_tools import user_exists
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import ugettext, ugettext_lazy as _
from django import forms


class EmailUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    username = forms.CharField(label=_("Username"), max_length=30,
                                help_text=_("Required. 30 characters or fewer."))
    email = forms.EmailField(label=_("Email"), max_length=75)

    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = get_user_model()
        fields = ("username", "email")

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        username = re.sub(r'\s', ' ', username).strip()
        if not username:
            raise forms.ValidationError('username is required', code='username_missing')
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        email = email.replace(' ', '').lower()

        if not email:
            raise forms.ValidationError(_("email is required"))

        if user_exists(email):
            raise forms.ValidationError(_("A user with that email already exists."))

        try:
            validate_email(email)
        except ValidationError as e:
            raise forms.ValidationError(_("the email is not a valid email form."))

        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(EmailUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user