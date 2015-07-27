from django import forms
from django.forms.widgets import HiddenInput

from .models import *


from django.forms.models import modelformset_factory

# creating a FormSet for a specific Model is easy
SubscriptionSettingsFormSetBase = modelformset_factory(
  EmailCategorySubscriptionSettings, 
  extra=0, 
  fields=('parent', 'category', 'status')
)

# now we want to add a checkbox so we can do stuff to only selected items
class SubscriptionSettingsFormSet(SubscriptionSettingsFormSetBase):
  def add_fields(self, form, index):

    super(SubscriptionSettingsFormSet, self).add_fields(form, index)

    choices = (
      (EmailCategorySubscriptionSettings.SUBSCRIBED, "Subscribed"),
      (EmailCategorySubscriptionSettings.UNSUBSCRIBED, "Unsubscribed")
    )
    form.fields['status'].widget = forms.RadioSelect(choices=choices)
    form.fields['category'].widget = forms.HiddenInput()
    form.fields['parent'].widget = forms.HiddenInput()

