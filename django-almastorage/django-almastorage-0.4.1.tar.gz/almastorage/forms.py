from django import forms
from .models import SwiftFile


class SwiftFileForm(forms.ModelForm):
	filefield = forms.FileField()

	class Meta:
		model = SwiftFile