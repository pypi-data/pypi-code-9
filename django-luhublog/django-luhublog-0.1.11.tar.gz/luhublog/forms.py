# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Button, Submit, HTML, Reset, Div
from crispy_forms.bootstrap import FormActions

from froala_editor.widgets import FroalaEditor

from luhublog.models import Author, Entry

class EntryForm(forms.ModelForm):
	content = forms.CharField(
					label="Contenido",
					required=True,
					widget=FroalaEditor(
						options={
							'height': '500',
							'fullPage': 'true',
							'trackScroll': 'true'
						}
					))

	class Meta:
		model = Entry
		fields = ['title', 'slug', 'image_caption', 'image_header', 'lead_entry', 'content', 'status', 'author', 'related' ]

	def __init__(self, *args, **kwargs):
		super(EntryForm, self).__init__(*args, **kwargs)
		self.fields['author'].queryset = Author.activated.all()

		self.helper = FormHelper()
		self.helper.layout = Layout(
			
			Div(
				'title',
				'slug',
				'lead_entry',
				'content',
				css_class="mrg-b-lg"

			),
			HTML("<h3><span>Imagenes</span></h3>"),
			Div(
				'image_caption',
				'image_header',
				css_class="mrg-b-lg"
			),
			HTML("<h3><span>Publicacion</span></h3>"),
			Div(
				'status',
				'author',
				'related',
				css_class="mrg-b-lg"
			),
			
			FormActions(
				Submit('save', _('Save'), css_class="btn-primary btn-lg"),
				css_class="text-center"
			)

		)