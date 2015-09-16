from django.forms.utils import ErrorDict


class BaseForm(object):
    def __init__(self, data=None, files=None):
        self._data = data or {}
        self._files = files or {}
        self._errors = None  #Stores the errors after clean() has been called.

    def is_valid(self):
        return self.is_bound and not self.errors

    @property
    def is_bound(self):
        return all(form.is_bound for form in self._subforms)

    @is_bound.setter
    def is_bound(self, value):
        for form in self._subforms:
            form.is_bound = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        for form in self._subforms:
            form.data = value
        self._data = value

    def _get_error_key(self, prefix, name):
        if prefix is None:
            return name

        return '{0}-{1}'.format(prefix, name)

    @property
    def errors(self):
        _errors = ErrorDict()
        for form in self._subforms:
            _errors.update({self._get_error_key(form.prefix, name): error for name, error in form.errors.items()})

        return _errors

    def __iter__(self):
        for name in self._field_name_mapper.keys():
            yield self[name]