from django import forms
from django.db import models


class Form1(forms.Form):
    field1 = forms.CharField(label='field1')
    field2 = forms.IntegerField(label='field2')

    def __init__(self, *args, custom_parameter=None, **kwargs):
        super(Form1, self).__init__(*args, **kwargs)
        self.param1 = custom_parameter


class Model(models.Model):
    field1 = models.IntegerField()


class ModelForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = ['field1']