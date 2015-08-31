# -*- coding: utf-8 -*-

__author__ = 'marcos.medeiros'

from django import forms

from rapid.models import Profile, Application
from rapid.wrappers import FieldData
from rapid.widgets import RapidReadOnly, RapidRelationReadOnly, RapidSelector

class ManageUsers(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'application': RapidRelationReadOnly(Application),
            'name': RapidReadOnly(),
            'description': RapidReadOnly,
            'users': RapidSelector(FieldData.from_model(Profile, 'users'))
        }
