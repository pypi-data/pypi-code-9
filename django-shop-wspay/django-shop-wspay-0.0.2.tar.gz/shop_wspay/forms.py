# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms


class WSPayForm(forms.Form):
    ShopID = forms.CharField(widget=forms.HiddenInput)
    ShoppingCartID = forms.CharField(widget=forms.HiddenInput)
    TotalAmount = forms.CharField(widget=forms.HiddenInput)
    Signature = forms.CharField(widget=forms.HiddenInput)
    ReturnURL = forms.CharField(widget=forms.HiddenInput)
    CancelURL = forms.CharField(widget=forms.HiddenInput)
    ReturnErrorURL = forms.CharField(widget=forms.HiddenInput)
