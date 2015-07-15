from wtforms_alchemy import model_form_factory
from .forms import Form, SecureForm

ModelForm = model_form_factory(Form)
SecureModelForm = model_form_factory(SecureForm)
