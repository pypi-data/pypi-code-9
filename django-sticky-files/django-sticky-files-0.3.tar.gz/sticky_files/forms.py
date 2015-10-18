# coding: utf-8

from django import forms


class UploadImageForm(forms.Form):
    file = forms.ImageField()


class UploadFileForm(forms.Form):
    file = forms.FileField()
