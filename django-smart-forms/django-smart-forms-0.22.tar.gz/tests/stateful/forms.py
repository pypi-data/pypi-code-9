from django import forms

from smartforms import StatefulForm


class TestStatefulForm(StatefulForm):
    VALUE2_CHOICES = (
        ('1', 'One'),
        ('2', 'Two'),
    )
    value1 = forms.CharField()
    value2 = forms.ChoiceField(choices=VALUE2_CHOICES)
