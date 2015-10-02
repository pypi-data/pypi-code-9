from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import ugettext, ugettext_lazy as _

from .models import EmailUserModel

# We need to override the base User creation and change forms
# because they are hard coded to use the User model, we just
# need to make them use our EmailUserModel model


# Override the forms:
class EmailUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("email", )

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            self._meta.model._default_manager.get(username=username)
        except self._meta.model.DoesNotExist:
            return username

        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_email(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            self._meta.model._default_manager.get(email=email)
        except self._meta.model.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])


class EmailUserChangeForm(UserChangeForm):
    """Docstring for EmailUserChangeForm """
    class Meta:
        model = get_user_model()
        # fields = UserChangeForm.Meta.fields
        fields = ("email", )


# Add the forms to our Admin class
class EmailUserAdmin(UserAdmin):

    form = EmailUserChangeForm
    add_form = EmailUserCreationForm
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('username', 'first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(EmailUserModel, EmailUserAdmin)
