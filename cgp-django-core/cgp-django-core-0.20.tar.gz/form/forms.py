# -*- coding: utf-8 -*-
import re

from django import forms
from django.forms.forms import BoundField
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe
from django.utils.encoding import smart_text, force_text, python_2_unicode_compatible
from django.utils import six

from django.core.exceptions import ImproperlyConfigured

from django.template import loader
from django.template import Context, Template
from django.utils.html import conditional_escape, format_html

class BoundField( BoundField ):
    def as_widget(self, widget=None, attrs=None, only_initial=False):

        """
        Renders the field by rendering the passed widget, adding any HTML
        attributes passed as attrs.  If no widget is specified, then the
        field's default widget will be used.
        """
        if not widget:
            widget = self.field.widget

        if self.field.localize:
            widget.is_localized = True

        attrs = attrs or {}
        auto_id = self.auto_id
        if auto_id and 'id' not in attrs and 'id' not in widget.attrs:
            if not only_initial:
                attrs['id'] = auto_id
            else:
                attrs['id'] = self.html_initial_id

        if not only_initial:
            name = self.html_name
        else:
            name = self.html_initial_name

        #OVERRIDE HERE TO SET BOUND FIELD
        widget.bound_field = self

        return force_text(widget.render(name, self.value(), attrs=attrs))

class Form( forms.Form ):

    form_render_template = 'forms/partials/form.html'

    def __getitem__(self, name):
        try:
            field = self.fields[name]
        except KeyError:
            raise KeyError(
                "Key %r not found in '%s'" % (name, self.__class__.__name__))

        #OVERRIDE HERE TO USE MONO BOUND FIELD INSTEAD
        return BoundField(self, field, name)

    def get_form_template(self):
        #Can be overridden for more complex logic
        if not self.form_render_template:
          raise ImproperlyConfigured('self.form_render_template not defined on form class')

        return self.form_render_template

    def render(self):
        
        #step 1: Output non-field errors


        #step 2: Output non-hidden fields
        #form html, form data, form validation

        #Step 3: Output hidden fields

        template_filename = self.get_form_template()
        context_data = {
            'form':self,
            'non_field_errors':self.non_field_errors(),
            'hidden_fields':self.get_hidden_fields(),
            'visible_fields':self.get_visible_fields()
        }
        context = Context(context_data)
        template = loader.get_template(template_filename)

        return template.render(context)

    def get_action_url(self):
        #OVERRIDE IN SUBCLASS
        return '.'

    def get_method(self):
        return "POST"

    def get_hidden_fields(self):
        output = []
        for name, field in self.fields.items():
            html_class_attr = ''
            field = self[name]
            if field.is_hidden:
                output.append(field)

        return output

    def get_visible_fields(self):
        output = []
        for name, field in self.fields.items():
            html_class_attr = ''
            field = self[name]
            if field.is_hidden==False:
                output.append(field)

        return output

    
    
    def _html_output(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
        "Helper function for outputting HTML. Used by as_table(), as_ul(), as_p()."
        top_errors = self.non_field_errors()  # Errors that should be displayed above all fields.
        output, hidden_fields = [], []

        for name, field in self.fields.items():
            html_class_attr = ''
            bf = self[name]
            # Escape and cache in local variable.
            bf_errors = self.error_class([conditional_escape(error) for error in bf.errors])
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend(
                        [_('(Hidden field %(name)s) %(error)s') % {'name': name, 'error': force_text(e)}
                         for e in bf_errors])
                hidden_fields.append(six.text_type(bf))
            else:
                # Create a 'class="..."' attribute if the row should have any
                # CSS classes applied.
                css_classes = bf.css_classes()
                if css_classes:
                    html_class_attr = ' class="%s"' % css_classes

                if errors_on_separate_row and bf_errors:
                    output.append(error_row % force_text(bf_errors))

                if bf.label:
                    label = conditional_escape(force_text(bf.label))
                    label = bf.label_tag(label) or ''
                else:
                    label = ''

                if field.help_text:
                    help_text = help_text_html % force_text(field.help_text)
                else:
                    help_text = ''

                output.append(normal_row % {
                    'errors': force_text(bf_errors),
                    'label': force_text(label),
                    'field': six.text_type(bf),
                    'help_text': help_text,
                    'html_class_attr': html_class_attr,
                    'field_name': bf.html_name,
                })

        if top_errors:
            output.insert(0, error_row % force_text(top_errors))

        if hidden_fields:  # Insert any hidden fields in the last row.
            str_hidden = ''.join(hidden_fields)
            if output:
                last_row = output[-1]
                # Chop off the trailing row_ender (e.g. '</td></tr>') and
                # insert the hidden fields.
                if not last_row.endswith(row_ender):
                    # This can happen in the as_p() case (and possibly others
                    # that users write): if there are only top errors, we may
                    # not be able to conscript the last row for our purposes,
                    # so insert a new, empty row.
                    last_row = (normal_row % {'errors': '', 'label': '',
                                              'field': '', 'help_text': '',
                                              'html_class_attr': html_class_attr})
                    output.append(last_row)
                output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
            else:
                # If there aren't any rows in the output, just append the
                # hidden fields.
                output.append(str_hidden)
        return mark_safe('\n'.join(output))
        
    def as_div_fields(self):
        "Returns this form rendered as HTML <tr>s -- excluding the <table></table>."
        return self._html_output(
            normal_row='\
              <div class="field">\
                <div class="inner">\
                  <div class="label">%(label)s</div>\
                  <div class="input">%(errors)s%(field)s%(help_text)s</div>\
                </div>\
              </div>',
            error_row='<span class="error-message">%s</span>',
            row_ender='</ender>',
            help_text_html='<span class="message">%s</span>',
            errors_on_separate_row=False)