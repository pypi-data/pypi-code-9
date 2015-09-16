from django import forms


class Form1(forms.Form):
    field1 = forms.CharField(required=True)


class Form1Dedup(forms.Form):
    field1 = forms.IntegerField()


class Form2(forms.Form):
    field2 = forms.CharField(required=True)
