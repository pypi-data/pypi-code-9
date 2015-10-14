# -#- coding: utf-8 -#-

from crispy_forms.bootstrap import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from django.db import models
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from form_designer.models import FormContent
from leonardo.module.web.models import Widget


class FormWidget(Widget, FormContent):

    form_layout = models.TextField(
        _('Form Layout'), blank=True, null=True,
        help_text=_('Crispy Form Layout see \
            http://django-crispy-forms.readthedocs.org/en/latest/layouts.html'))

    class Meta:
        abstract = True
        verbose_name = _('form')
        verbose_name_plural = _('forms')

    def process_valid_form(self, request, form_instance, **kwargs):
        """ Process form and return response (hook method). """
        return render_to_string(self.template, context)

    def render(self, request, **kwargs):
        context = RequestContext(
            request, {'widget': self})

        form_class = self.form.form()

        prefix = 'fc%d' % self.id
        formcontent = request.POST.get('_formcontent')

        if request.method == 'POST' and (
                not formcontent or formcontent == smart_text(self.id)):
            form_instance = form_class(request.POST, prefix=prefix)

            if form_instance.is_valid():
                process_result = self.form.process(form_instance, request)
                context = RequestContext(
                    request,
                    {
                        'widget': self,
                        'message': self.success_message or process_result or u'',
                    }
                )
        else:
            form_instance = form_class(prefix=prefix)

            # use crispy forms
            form_instance.helper = FormHelper(form_instance)
            form_instance.helper.form_action = '#form{}'.format(self.id)

            if self.form_layout:

                try:
                    form_instance.helper.layout = eval(self.form_layout)
                except Exception as e:
                    raise e

            else:
                # use default layout
                if self.show_form_title:
                    form_instance.helper.layout = Layout(
                        Fieldset(self.form.title,
                                 *form_instance.fields.keys()),
                    )
                else:
                    form_instance.helper.layout = Layout(
                        *form_instance.fields.keys()
                    )
                form_instance.helper.layout.extend([ButtonHolder(
                    Submit('submit', 'Submit', css_class='button white')
                )
                ])

            context['form'] = form_instance

        return render_to_string(self.get_template_name, context)
