from django import forms

from . import models


class IPNReceiverForm(forms.ModelForm):

    class Meta:
        model = models.MpesaPayment
        fields = "__all__"

    def clean_original(self):
        data = self.cleaned_data["original"]
        # Remove data that we don't need to store
        del data["user"]
        del data["pass"]
        return data
