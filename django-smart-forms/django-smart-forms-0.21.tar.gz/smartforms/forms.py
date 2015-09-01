from copy import deepcopy
from collections import OrderedDict
from django.forms.utils import ErrorDict


class BaseForm(object):
    def is_valid(self):
        return all(form.is_bound and not form.errors for form in self._subforms)

    @property
    def is_bound(self):
        return all(form.is_bound for form in self._subforms)

    def __iter__(self):
        for name in self._field_name_mapper.keys():
            yield self[name]


class CompositeForm(BaseForm):
    def __init__(self, data=None, files=None, form_classes=[], form_instances=[]):
        if len(form_instances) and len(form_classes):
            raise AttributeError('form_classes and form_instances could not be setted')

        self.form_classes = form_classes
        self._subforms = deepcopy(form_instances)
        self._field_name_mapper = {}

        ## Initialize forms if they defined by classes
        for i in range(0, len(self.form_classes)):
            form = self.form_classes[i](data, files)
            self._subforms.append(form)

        ## Fill up the field mapper
        for i in range(0, len(self._subforms)):
            for name in self._subforms[i].fields.keys():
                self._field_name_mapper[name] = i

    def __getitem__(self, name):
        "Returns a BoundField with the given name."
        try:
            name not in self._field_name_mapper.keys()
        except KeyError:
            raise KeyError(
                "Key %r not found in '%s'" % (name, self.__class__.__name__))

        return self._subforms[self._field_name_mapper[name]][name]

    @property
    def fields(self):
        retval = OrderedDict()
        for form in self._subforms:
            retval.update(form.fields)
        return retval

    @property
    def errors(self):
        _errors = ErrorDict()
        for form in self._subforms:
            _errors.update(form.errors)
        return _errors


class FormSet(BaseForm):
    def __init__(self, data=None, files=None, form_class=None, repeat=1, min_valid=None, **kwargs):
        self._subforms = []
        self._field_name_mapper = OrderedDict()

        if min_valid is None:
            min_valid = repeat

        ## Initialize subforms
        for i in range(0, repeat):
            prefix = 'form{0}'.format(i)
            kwargs['prefix'] = prefix
            if i + 1 > min_valid:
                kwargs['empty_permitted'] = True
            kwargs = self._update_kwargs(kwargs, i)
            obj = form_class(data, files, **kwargs)
            self._subforms.append(obj)

        ## Fill up the field mapper
        for i in range(0, len(self._subforms)):
            for name in self._subforms[i].fields.keys():
                prefix = 'form{0}'.format(i)
                self._field_name_mapper['{0}-{1}'.format(prefix, name)] = i

    def __getitem__(self, name):
        """ Returns a BoundField with the given name. """
        try:
            name not in self._field_name_mapper.keys()
        except KeyError:
            raise KeyError(
                "Key %r not found in '%s'" % (name, self.__class__.__name__))

        subname = name.split('-', 1)[1]
        return self._subforms[self._field_name_mapper[name]][subname]

    def _update_kwargs(self, kwargs, i):
        return kwargs

    @property
    def fields(self):
        retval = OrderedDict()
        for form in self._subforms:
            prefix = form.prefix
            retval.update({'{0}-{1}'.format(prefix, name): field for name, field in form.fields.items()})
        return retval

    @property
    def errors(self):
        _errors = ErrorDict()
        for form in self._subforms:
            prefix = form.prefix
            _errors.update({'{0}-{1}'.format(prefix, name): error for name, error in form.errors.items()})
        return _errors