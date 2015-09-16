from copy import deepcopy
from collections import OrderedDict

from .base import BaseForm


class CompositeForm(BaseForm):
    def __init__(self, data=None, files=None, form_classes=[], form_instances=[]):
        if len(form_instances) and len(form_classes):
            raise AttributeError('form_classes and form_instances could not be setted')

        super().__init__(data or {}, files or {})

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

        if data is None:
            self._data = self._subforms[0].data

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
