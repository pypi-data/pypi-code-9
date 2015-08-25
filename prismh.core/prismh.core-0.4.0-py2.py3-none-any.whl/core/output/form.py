#
# Copyright (c) 2015, Prometheus Research, LLC
#


from .common import SortedDict, TypedSortedDict, TypedDefinedOrderDict, \
    InstrumentReference, Descriptor


__all__ = (
    'Form',
)


class Event(TypedDefinedOrderDict):
    order = [
        'trigger',
        'action',
        'targets',
        'options',
    ]

    key_types = {
        'options': SortedDict,
    }


class Widget(TypedDefinedOrderDict):
    order = [
        'type',
        'options',
    ]

    key_types = {
        'options': SortedDict,
    }


class ElementOptions(TypedDefinedOrderDict):
    order = [
        'fieldId',
        'text',
        'help',
        'error',
        'audio',
        'enumerations',
        'questions',
        'rows',
        'widget',
        'events',
    ]

    key_types = {
        'text': SortedDict,
        'help': SortedDict,
        'error': SortedDict,
        'audio': SortedDict,
        'enumerations': [Descriptor],
        'rows': [Descriptor],
        'widget': Widget,
        'events': [Event],
    }

ElementOptions.key_types['questions'] = [ElementOptions]


class Element(TypedDefinedOrderDict):
    order = [
        'type',
        'tags',
        'options',
    ]

    key_types = {
        'options': ElementOptions,
    }


class Page(TypedDefinedOrderDict):
    order = [
        'id',
        'elements',
    ]

    key_types = {
        'elements': [Element],
    }


class Unprompted(TypedDefinedOrderDict):
    order = [
        'action',
        'options',
    ]

    key_types = {
        'options': SortedDict,
    }


class UnpromptedCollection(TypedSortedDict):
    subtype = Unprompted


class Parameter(TypedDefinedOrderDict):
    order = [
        'type',
    ]


class ParameterCollection(TypedSortedDict):
    subtype = Parameter


class Form(TypedDefinedOrderDict):
    order = [
        'instrument',
        'defaultLocalization',
        'title',
        'pages',
        'unprompted',
        'parameters',
    ]

    key_types = {
        'instrument': InstrumentReference,
        'title': SortedDict,
        'pages': [Page],
        'unprompted': UnpromptedCollection,
        'parameters': ParameterCollection,
    }

