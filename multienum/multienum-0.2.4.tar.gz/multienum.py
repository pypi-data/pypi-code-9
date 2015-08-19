"""MultiEnum class for enumerations for multiple equivalent names.

Full documentation is in the README.  At present, this has only been tested in
CPython 3.4, although it should work for any recent version which allows
subclassing of the core int type.

"""

# pylint: disable=W0212,E1101

class MultiEnum(int):
    """Enumeration type as int sublcass with support for multiple names

    :cvar sequence _members: Sequence of members defining enumerated names
    :cvar sequence _fields: Names corresponding to the position within the
    member sequences

    :ivar str name: The default (first) name defined for the given value

    >>> class SampleEnum(MultiEnum):
    ...   _members = (("zero", "zip", "zero", "cero"),
    ...               ("one", "ace", "une", "uno"),
    ...               ("two", "deuce", "deux", "dos"))
    ...   _fields = ('english', 'slang', 'french', 'spanish')
    >>> val1 = SampleEnum("one")
    >>> int(val1)
    1
    >>> str(val1)
    'one'
    >>> val1.name
    'one'
    >>> val1.spanish
    'uno'
    >>> val2 = SampleEnum(slang="deuce")
    >>> int(val2)
    2

    Each instance of MultiEnum also can be iterated as name, value tuples,
    making the following construction possible:

    >>> enum_dict = dict(SampleEnum('two'))
    >>> enum_dict['french']
    'deux'

    To facilitate use of MultiEnum with Django objects as an argument to the
    'choices' parameter, the _choices() method is available as long as the
    _fields attribute is defined on the class.  By default, the first two
    parameters are returned.  To use a different set of fields, the
    ;_choice_fields; parameter can be set as a two-tuple of field names.  To
    use the enumerated value as one of the choices, use the virtual field name
    '_enum'.  A reduced set of choices can also be picked by setting the
    '_choice_range' attribute to a two-tuple with a start and end range (using
    the same semantics as an array range start and end index).

    >>> SampleEnum._choices()
    (('zero', 'zip'), ('one', 'ace'), ('two', 'deuce'))
    >>> class SampleChoicesEnum(SampleEnum):
    ...   _choice_fields = ('_enum', 'french')
    ...   _choice_range = (1,3)
    >>> SampleChoicesEnum._choices()
    ((1, 'une'), (2, 'deux'))

    """
    _members = None
    _fields = None

    @classmethod
    def _resolve_value(cls, val):
        if type(val) is cls:
            # Already an enum
            return val
        if type(val) is int:
            intval = val
        else:
            try:
                intval = next(i for i in range(0, len(cls._members))
                              if str(val) in cls._members[i])
            except StopIteration:
                raise AttributeError(
                    "Enumeration name '%s' not in _members" % val)

        return intval

    def __new__(cls, *args, **kwargs):
        if cls._members is None:
            raise TypeError("No _members given at definition")

        if len(args) + len(kwargs) != 1:
            raise TypeError(
                "Enumeration creation takes exactly one parameter")

        if args:
            retval = cls._resolve_value(args[0])

        for key, val in kwargs.items():
            findex = tuple(cls._fields).index(key)
            retval = tuple(m[findex] for m in cls._members).index(val)

        if type(retval) is not cls:
            retval = super(MultiEnum, cls).__new__(cls, retval)
            retval._names = tuple(cls._members[int(retval)])
        return retval

    def __getattr__(self, key):
        if self._fields is None:
            raise AttributeError(
                "Attribute missing: MultiEnum object does not have _fields defined")

        if key in self._fields:
            index = self._fields.index(key)
        else:
            raise AttributeError("Enumeration name '%s' not defined" % key)

        return self._names[index]

    @classmethod
    def _choices(cls):
        (rs, re) = getattr(cls, '_choice_range', (0, len(cls._members)))
        series = []
        fields = cls._fields or (0, 1)
        for f in getattr(cls, '_choice_fields', (fields[0], fields[1])):
            if f == '_enum':
                series.append(range(0, len(cls._members)))
            else:
                ind = fields.index(f)
                series.append(tuple(m[ind] for m in cls._members))
        return tuple(zip(series[0][rs:re], series[1][rs:re]))

    @property
    def name(self):
        """Default name for number"""
        return self._names[0]

    def __iter__(self):
        return (z for z in zip(self._fields, self._members[self]))

    def __str__(self):
        return self._names[0]

    def __repr__(self):
        return "'%s'"  % self._names[0]

