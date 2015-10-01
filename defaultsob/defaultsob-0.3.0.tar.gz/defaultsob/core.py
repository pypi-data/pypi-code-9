# -*- coding: utf-8 -*-


def ordered_set(iter):
    """Creates an ordered set

    @param iter: list or tuple
    @return: list with unique values

    """
    final = []
    for i in iter:
        if i not in final:
            final.append(i)

    return final


def class_slots(ob):
    """Get object attributes from child class attributes

    @param ob: Defaults object
    @type ob: Defaults
    @return: Tuple of slots

    """
    current_class = type(ob).__mro__[0]
    if not getattr(current_class, 'allslots', None) \
            and current_class != object:
        _allslots = [list(getattr(cls, '__slots__', []))
                     for cls in type(ob).__mro__]
        _fslots = []
        for slot in _allslots:
            _fslots = _fslots + slot
        current_class.allslots = tuple(ordered_set(_fslots))
    return current_class.allslots


def use_if_none_cls(alternative_attr):
    def use_if_none(original_attr, ob, kwargs):
        """
        Try and get a value from kwargs for original_attr.  If there
        is no original_attr in kwargs use the alternative_attr value 
        in the object ob

        @param alternative_attr: the alternative attribute 
        @param original_attr: the original attribute
        @param ob: the object with the attributes 
        @param kwargs: key values
        @return: final value 
        """
        return kwargs.get(original_attr, getattr(ob, alternative_attr, None))
    return use_if_none


def usef(attr):
    """Use another value as default

    @param attr: the name of the attribute to
                use as alternative value
    @return: value of alternative attribute

    """
    return use_if_none_cls(attr)

use_name_if_none = usef('Name')


def choose_alt(attr, ob, kwargs):
    """If the declared class attribute of ob is callable
    then use that callable to get a default ob 
    instance value if a value is not available in kwargs.

    @param attr: ob class attribute name
    @param ob: the object instance whose default value needs to be set
    @param kwargs: the kwargs values passed to the ob __init__ method
    @return: value to be used to set ob instance

    """
    result = ob.__class__.__dict__.get(attr, None)
    if type(result).__name__ == "member_descriptor":
        result = None
    elif callable(result):
        result = result(attr, ob, kwargs)
    return result


class Defaults(object):

    """A base class which allows using slots to define 
    attributes and the ability to set object 
    instance defaults at the child class level"""

    def __init__(self, **kwargs):
        """Assign kwargs to attributes and defaults to attributes"""

        allslots = class_slots(self)
        for attr in allslots:
            setattr(self, attr, kwargs.get(
                attr, choose_alt(attr, self, kwargs)))

    def to_dict(self):
        """Returns attributes with values as dict
        @return: dictionary of attributes with values
        """

        allslots = class_slots(self)
        return {
            item: getattr(self, item, None)
            for item in allslots
        }

    def to_dict_clean(self):
        """Return a dict where there values of None 
        are not included
        @return: dict of the object properties with values
        """
        attribs = self.to_dict()
        return {
            k: v
            for k, v in attribs.items() if v
        }
