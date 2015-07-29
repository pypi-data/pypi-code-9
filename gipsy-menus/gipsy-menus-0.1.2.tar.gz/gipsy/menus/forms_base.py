from django import forms
from django.core.validators import URLValidator
from django.utils.translation import ugettext_lazy as _
from mptt.forms import MPTTAdminForm
from optionsfield.fields import OptionsFormField, OptionsWidget


class MenuNodeAdminFormBase(MPTTAdminForm):

    options = OptionsFormField(widget=OptionsWidget())

    def __init__(self, *args, **kwargs):
        super(MenuNodeAdminFormBase, self).__init__(*args, **kwargs)

    def clean_url(self):
        url = self.cleaned_data.get('url')
        if url:
            try:
                URLValidator()(url)
            except forms.ValidationError:
                if not (url.startswith('/') or url.startswith('#')):
                    url = "/" + url
                URLValidator()('http://example.com{}'.format(url))
        return url

    def _validate_stub_and_parent(self):
        stub = self.cleaned_data.get('stub')
        parent = self.cleaned_data.get('parent')

        if stub and parent:
            error = _(u"You can only select stub or select parent node")
            self.add_error('stub', error)
            self.add_error('parent', error)

        if not (stub or parent):
            error = _(u"You must select stub or parent node")
            self.add_error('stub', error)
            self.add_error('parent', error)

    def _validate_url_and_content_object(self, url_field='url'):
        stub = self.cleaned_data.get('stub')
        url = self.cleaned_data.get(url_field)
        content_type = self.cleaned_data.get('content_type')
        object_id = self.cleaned_data.get('object_id')

        if stub and (url or content_type or object_id):
            error = _("You cannot provide url or select internal object when node has stub selected")
            if url:
                self.add_error(url_field, error)
            if content_type:
                self.add_error('content_type', error)
            if object_id:
                self.add_error('object_id', error)

        if not stub and not (url or content_type or object_id):
            error = _("You must provide url or select internal object")
            self.add_error(url_field, error)
            self.add_error('content_type', error)
            self.add_error('object_id', error)

        # if not (stub or (url and (content_type or object_id))):
        if not stub and (url and (content_type or object_id)):
            error = _("You can only provide url or select internal object")
            self.add_error(url_field, error)
            if content_type:
                self.add_error('content_type', error)
            if object_id:
                self.add_error('object_id', error)

    def _validate_content_object(self):
        content_type = self.cleaned_data.get('content_type')
        object_id = self.cleaned_data.get('object_id')

        if not content_type and object_id:
            error = _("Select content type")
            self.add_error('content_type', error)

        if not object_id and content_type:
            raise forms.ValidationError("Select object id")
            self.add_error('object_id', error)

    def clean(self):
        self._validate_stub_and_parent()
        self._validate_url_and_content_object()
        self._validate_content_object()
        return super(MenuNodeAdminFormBase, self).clean()
