from bs4 import BeautifulSoup
from django import forms
from django.utils.encoding import force_text

from django.forms.utils import flatatt, to_current_timezone
from django.forms.widgets import TextInput as BaseTextInput
from django.forms.widgets import Textarea as BaseTextarea
from django.forms.widgets import CheckboxInput as BaseCheckboxInput
from django.forms.widgets import Select as BaseSelect
from django.forms.widgets import SelectMultiple as BaseSelectMultiple
from django.forms.widgets import ClearableFileInput as BaseClearableFileInput
from django.forms.widgets import RadioSelect as BaseRadioSelect
from django.forms.widgets import CheckboxSelectMultiple as BaseCheckboxSelectMultiple

from django.core.exceptions import ImproperlyConfigured
from django.utils.safestring import mark_safe

from django.template import loader
from django.template import Context, Template
from django.utils.html import conditional_escape, format_html

def pretty_html(html):
  soup = BeautifulSoup(html, 'html.parser')
  return soup.prettify()
  

class BaseFormWidget(object):
  has_custom_render = True
  bound_field = None
  

  def __init__(self, attrs=None):
    if attrs is not None:
      self.attrs = attrs.copy()
    else:
      self.attrs = {}

  def get_file_template(self):
    #Can be overridden for more complex logic
    if not self.file_template:
      raise ImproperlyConfigured('self.file_template not defined on widget class')

    return self.file_template

  def mono_render_input(self, field, name, value, attrs=None):
    context = {'field':field, 'name':name,'value':value, 'attrs':attrs}
    return self.render_input(final_attrs, context)

  def render_input(self, context_data):
    template_filename = self.get_file_template()

    context = Context(context_data)

    if self.bound_field:
      context['field'] = self.bound_field


    template = loader.get_template(template_filename)
    
    rendered = template.render(context)

    #Make it pretty:
    return mark_safe(pretty_html(rendered))


class TextInputWidget(BaseFormWidget, BaseTextInput):
  input_type = 'text'
  file_template = 'forms/partials/textfield.html'

  def render(self, name, value, attrs=None):

    context = self.build_attrs(attrs, type=self.input_type, name=name)
    if value != '':
      # Only add the 'value' attribute if a value is non-empty.
      context['value'] = force_text(self._format_value(value))
    
    return self.render_input(context)

class HoneypotWidget(TextInputWidget):
  file_template = 'forms/partials/honeypot.html'

class TextareaWidget(BaseFormWidget, BaseTextarea):
  file_template = 'forms/partials/textarea.html'

  def render(self, name, value, attrs=None):

    context = self.build_attrs(attrs, name=name)
    if value:
      context['value'] = value

    return self.render_input(context)

class CheckboxInputWidget(BaseFormWidget, BaseCheckboxInput):
  file_template = 'forms/partials/checkbox.html'

  def check_test(self, v):
    return not (v is False or v is None or v == '')

  def render(self, name, value, attrs=None):

    if self.check_test(value):
      attrs['checked'] = 'checked'

    context = self.build_attrs(attrs, name=name)
    
    if not (value is True or value is False or value is None or value == ''):
      context['value'] = force_text(value)
    return self.render_input(context)


class CheckboxSelectWidget(BaseFormWidget, BaseCheckboxSelectMultiple):
  file_template = 'forms/partials/input_group.html'

  def render(self, name, value, attrs=None):

    context = self.build_attrs(attrs, name=name)
    context['value'] = value
    return self.render_input(context)

class RadioSelectWidget(BaseFormWidget, BaseRadioSelect):
  file_template = 'forms/partials/input_group.html'

  def render(self, name, value, attrs=None):

    context = self.build_attrs(attrs, name=name)
    context['value'] = value
    context['radio'] = True
    return self.render_input(context)

class SelectWidget(BaseFormWidget, BaseSelect):
  file_template = 'forms/partials/select.html'

  def render(self, name, value, attrs=None):

    context = self.build_attrs(attrs, name=name)
    context['value'] = value
    return self.render_input(context)


class SelectMultipleWidget(BaseFormWidget, BaseSelectMultiple):
  file_template = 'forms/partials/select.html'

  def render(self, name, value, attrs=None):

    context = self.build_attrs(attrs, name=name)
    context['value'] = value
    context['multiple'] = True
    return self.render_input(context)



class ClearableFileInputWidget(BaseFormWidget, BaseClearableFileInput):
  file_template = 'forms/partials/file.html'

  def render(self, name, value, attrs=None):

    context = self.build_attrs(attrs, name=name)
    context['value'] = value
    context['type'] = 'file'
    return self.render_input(context)



# class MultipleChoiceFieldWidget(forms.MultipleChoiceField):
#   file_template = 'forms/partials/input_group.html'

#   def valid_value(self, value):
    

#     if isinstance(value, (basestring)):
#       try:
#         value_as_list = eval(value)
#       except:
#         value_as_list = value
#     else:
#       value_as_list = value
    
#     choices_values = dict(self.choices).keys()
#     choices_values = [choice.strip() for choice in choices_values]
    
#     if isinstance(value_as_list, (list)) == False:
#       value_as_list = [value_as_list]
#       # print 'render to list %s'%(value_as_list)


#     for value_item in value_as_list:
#       found_match = False
      
#       for choice in choices_values:
#         if choice == value_item.strip():
#           found_match = True

#       if found_match == False:
#         print 'WARNING: Value %s-%s not in choices list %s'%(value, value_item, choices_values)
#         return False

#     return True

#   def prepare_value(self, value):
#     #suss out the field value
#     if value and (len(value)>0):
#       first_element = value[0]
#       if isinstance(first_element, (list)):
#         value = first_element

#     return value



