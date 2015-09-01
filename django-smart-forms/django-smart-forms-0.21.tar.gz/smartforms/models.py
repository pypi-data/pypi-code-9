from django.db import transaction

from .forms import BaseForm, CompositeForm, FormSet


class BaseModelForm(BaseForm):
    def save(self, commit=True):
        with transaction.atomic():
            for form in self._subforms:
                if form.empty_permitted and not form.has_changed():
                    continue
                form.save(commit=commit)


class CompositeModelForm(BaseModelForm, CompositeForm):
    def __init__(self, *args, **kwargs):
        super(CompositeModelForm, self).__init__(*args, **kwargs)
        if not all(hasattr(obj, 'save') for obj in self._subforms):
            raise ValueError('all form instance must have save method (model form)')


class ModelFormSet(FormSet, BaseModelForm):
    def __init__(self, data=None, files=None, form_class=None, repeat=1, instances=None, **kwargs):
        if not hasattr(form_class, 'save'):
            raise ValueError('form_class must be ModelForm')
        self._instances = instances
        super(ModelFormSet, self).__init__(data, files, form_class, repeat, **kwargs)

    def _update_kwargs(self, kwargs, i):
        try:
            kwargs['instance'] = self._instances[i]
        except (IndexError, TypeError):
            pass
        return kwargs