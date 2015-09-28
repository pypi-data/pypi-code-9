from django.db import models
from django.utils.translation import ugettext_lazy as _
from emencia.django.newsletter.forms import MailingListSubscriptionForm
from emencia.django.newsletter.models import MailingList
from leonardo.models import Widget
from django.template import RequestContext
from crispy_forms.helper import FormHelper


class SubscriptionFormWidget(Widget):

    """CMS Plugin for susbcribing to a mailing list"""
    title = models.CharField(_('title'), max_length=100, blank=True)
    show_description = models.BooleanField(_('show description'), default=True,
                                           help_text=_('Show the mailing list\'s description.'))
    mailing_list = models.ForeignKey(MailingList, verbose_name=_('mailing list'),
                                     help_text=_('Mailing List to subscribe to.'))

    def __unicode__(self):
        return self.mailing_list.name

    def render(self, **kwargs):
        request = kwargs['request']
        context = RequestContext(
            request,
            {
                'widget': self,
            }
        )
        form_name = self.fe_identifier

        if request.method == "POST" and (form_name in request.POST.keys()):
            form = MailingListSubscriptionForm(data=request.POST)
            if form.is_valid():
                form.save(self.mailing_list)
                form.saved = True
        else:
            form = MailingListSubscriptionForm()

        form.helper = FormHelper(form)
        form.helper.form_tag = False

        context.update({
            'object': self.mailing_list,
            'form': form,
            'request': request,
            'form_name': form_name,
        })
        return self.render_response(context)

    class Meta:
        abstract = True
        verbose_name = _('Newsletter Subscription Form')
        verbose_name_plural = _('Newsletter Subscription Forms')
