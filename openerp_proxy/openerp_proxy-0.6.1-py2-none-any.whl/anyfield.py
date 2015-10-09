import six

from .utils import ustr as _

import operator


@six.python_2_unicode_compatible
class FieldNotFoundException(Exception):
    """ Exception raised when HField cannot find field in object been processed
    """
    def __init__(self, obj, field, original_exc=None):
        self.field = field
        self.obj = obj
        self.orig_exc = original_exc

    @property
    def message(self):
        return u"Field %s not found in obj %s" % (_(self.field), _(self.obj))

    def __str__(self):
        # converting to ascii because of python's warnings module fails in
        # UnicodeEncodeError when no-ascii symbols present in str(exception)
        return self.message.encode('ascii', 'backslashreplace').decode()

    def __repr__(self):
        return str(self)


def to_fval(obj, rec):
    if isinstance(obj, FField):
        return obj.__getvalue__(rec)
    return obj


@six.python_2_unicode_compatible
class FField(object):
    """ Usage:

            field1 = F.my_field1.related_field[index].field3(arg1, arg2, arg4=4)

            for record in data:
                field1_val = field1.__getvalue__(record)
    """
    def __init__(self, field, *args, **kwargs):
        assert callable(field), "field must be callable"
        self._field = field

    @classmethod
    def inst(cls):
        return cls(lambda r: r)

    # Field specific methods
    def __getvalue__(self, record):
        return self._field(record)

    def __chain__(self, fn):
        return type(self)(fn)

    # Operators implemented
    def __call__(self, *args, **kwargs):
        # TODO: check if there are any FField instances in args
        return self.__chain__(lambda record: self.__getvalue__(record)(*args, **kwargs))

    def __getattr__(self, name):
        # TODO: check if name is FField instance
        return self.__chain__(lambda record: getattr(self.__getvalue__(record), name))

    def __getitem__(self, name):
        # TODO: check if name is FField instance
        return self.__chain__(lambda record: self.__getvalue__(record)[name])

    def __not__(self):
        return self.__chain__(lambda record: not self.__getvalue__(record))

    def __lt__(self, other):
        return self.__chain__(lambda record: self.__getvalue__(record) < other)

    def __le__(self, other):
        return self.__chain__(lambda record: self.__getvalue__(record) <= other)

    def __eq__(self, other):
        return self.__chain__(lambda record: self.__getvalue__(record) == other)

    def __ne__(self, other):
        return self.__chain__(lambda record: self.__getvalue__(record) != other)

    def __gt__(self, other):
        return self.__chain__(lambda record: self.__getvalue__(record) > other)

    def __ge__(self, other):
        return self.__chain__(lambda record: self.__getvalue__(record) >= other)

    def __str__(self):
        return "FField"

F = FField.inst()


@six.python_2_unicode_compatible
class HField(object):
    """ Describes how to get a field from data record.

        :param field: path to field or function to get value from record
                      if path is string, then it should be dot separated list of
                      fields/subfields to get value from. for example
                      ``sale_line_id.order_id.name`` or ``picking_id.move_lines.0.location_id``
        :type field: str | func(record)->value
        :param str name: name of field. (optional)
                            if specified, then this value will be used in column header of table.
        :param bool silent: If set to True, then not exceptions will be raised and *default* value
                            will be returned. (default=False)
        :param default: default value to be returned if field not found. default=None
        :param args: if specified, then it means that field is callable, and *args* should be passed
                     to it as positional arguments. This may be useful to call *as_html_table* method
                     of internal field. for example::

                         HField('picking_id.move_lines.as_html_table',
                                args=('id', '_name', HField('location_id._name', 'Location')))

                     or better way::

                         HField('picking_id.move_lines.as_html_table').with_args(
                             'id',
                             '_name',
                             HField('location_id._name', 'Location')
                         )

        :type args: list | tuple
        :param dict kwargs: same as *args* but for keyword arguments
    """

    def __init__(self, field, name=None, silent=False, default=None, args=None, kwargs=None):
        self._field = field
        self._name = name
        self._silent = silent
        self._default = default
        self._args = tuple() if args is None else args
        self._kwargs = dict() if kwargs is None else kwargs

    def with_args(self, *args, **kwargs):
        """ If field is string pointing to function (or method),
            all arguments and keyword arguments passed to this method,
            will be passed to field (function).

            For example::

                HField('picking_id.move_lines.as_html_table').with_args(
                    'id', '_name', HField('location_id._name', 'Location'))

            This arguments ('id', '_name', HField('location_id._name', 'Location'))
            will be passed to ``picking_id.move_lines.as_html_table`` method

            :return: self
        """
        self._args = args
        self._kwargs = kwargs
        return self

    @classmethod
    def _get_field(cls, obj, name):
        """ Try to get field named *name* from object *obj*
        """
        try:
            res = obj[name]
        except:
            try:
                res = obj[int(name)]
            except:
                try:
                    res = getattr(obj, name)
                except:
                    raise FieldNotFoundException(obj, name)
        return res

    def get_field(self, record):
        """ Returns requested value from specified record (object)

            :param record: Record instance to get field from (also should work on any other object)
            :type record: Record
            :return: requested value
        """

        if callable(self._field):
            return self._field(record, *self._args, **self._kwargs)

        fields = self._field.split('.')
        r = record
        while fields:
            field = fields.pop(0)
            try:
                r = self._get_field(r, field)
                if callable(r) and fields:  # and if attribute is callable and
                                            # it is not last field then call
                                            # it without arguments
                    r = r()
                elif callable(r) and not fields:  # last field and if is callable
                    r = r(*self._args, **self._kwargs)
            except:  # FieldNotFoundException:
                if not self._silent:   # reraise exception if not silent
                    raise
                else:                  # or return default value
                    r = self._default
                    break
        return r

    def __call__(self, record):
        """ Get value from specified record

            :param record: object to get field from
            :type record: Record
            :return: value of self-field of record
        """
        return self.get_field(record)

    def __str__(self):
        return _(self._name) if self._name is not None else _(self._field)
