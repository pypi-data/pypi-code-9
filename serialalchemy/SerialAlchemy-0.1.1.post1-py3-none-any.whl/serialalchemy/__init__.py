'''SerialAlchemy
Dead simple object serialization for SQLAlchemy

'''

from sqlalchemy import inspect, DateTime, Date, Time, processors, event
from decimal import Decimal
from datetime import datetime, date, timedelta, time

import re
from collections import abc
import json
import inspect as pyinspect

#from types import NoneType

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')
def convert_class(name):
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()

primitives = (int, str, bytes, float, dict, list, type(None),)

def _get_value(obj, field):
    global primitives

    value = getattr(obj, field)

    if isinstance(value, Decimal):
        return float(value)
    elif isinstance(value, datetime) or isinstance(value, date) or\
            isinstance(value, time):
        return str(value)
    elif isinstance(value, timedelta):
        return float(value.total_seconds())
    elif isinstance(value, (set, frozenset,)):
        return list(value)
    elif not isinstance(value, primitives):
        return str(value)

    return value



class Serializable:
    '''Provides serialization and deserialization for data-mapped classes.

    This is a mixin class that provides serializaiton to python dicts and 
    object population (deserialization). A method for creating a streaming 
    json generator from a result set is also defined.

    The mixin defines two special attributes during SQLAlchemy's 
    `mapper_configured` event which are used for json generation.

    :attribute __single__: The name of a single object. If not specified,
        the mapper class name is used, converting camel-case to
        underscore.

    :attribute __plural__: The name of multiple objects. If not specified,
        the mapper's `__tablename__` is used.

    This is my own personal preference, although I'm told a few other people do
    it this way too::
        class User(Base, Serializable):
            __tablename__ = 'users'

            #rest of class definition
        
    In this example, __single__ = 'user', __plural__ = 'users'.

    '''

    @classmethod
    def _define_special_fields(cls):
        if not hasattr(cls, '__single__') or cls.__single__ is None:
            cls.__single__ = convert_class(cls.__name__)

        if not hasattr(cls, '__plural__') or cls.__plural__ is None:
            if hasattr(cls, '__tablename__'):
                cls.__plural__ = cls.__tablename__
            else:
                cls.__plural__ = cls.__single__


    def to_dict(self, fields=None, relationships=True, mtm_pkonly=True):
        '''Serialize a SQLAlchemy mapper in to a python dictionary.
        
        :param fields=None: An iterable of field names (str) or None. 
            The dictionary returned will include only the fields specified.
            Alternatively, prefixing a field name with a tilde (~) will 
            exclude that field from the returned dict. Mixing included and
            excluded field names will ignore the excluded fields.
            
            Relationship properties can be in this parameter, although will be 
            ignored unless the `relationships` parameter is True. Properties of
            related objects are filtered via SQLAlchemy's `load_only` query
            option.

        :param relationships=True: Include or omit relationship properties.
            Output is based on the relationship definition. It will be either 
            a list of dicts, or a dict itself based on the `uselist` parameter
            of the relationship function.

            The `fields` paramter does not affect the related object output.
            To filter related object fields, use SQLAlchemy's `load_only` 
            device during query construction.

            The related class must also have the `Serializable` mixin.

            *Note: Relationships of related objects are ignored. I couldn't 
            see the benefit vs the complexity it would bring.*

        :param mtm_pkonly=True: If True, return only the primary-key for
            secondary objects of a many-to-many relationship. If False, 
            all fields of the secondary object will be included, subject
            to the `load_only` filter.
        '''

        output = {}

        includes = frozenset()
        excludes = frozenset()

        if fields is not None:
            includes = frozenset([f for f in fields if not f.startswith('~')])
            excludes = frozenset([f[1:] for f in fields if f.startswith('~')])
        
        info = inspect(self)


        for field, col in info.mapper.columns.items():
            if includes and field not in includes:
                continue
            elif excludes and field in excludes:
                continue

            output[field] = _get_value(self, field)


        if relationships:
            for field, relation in info.mapper.relationships.items():
                if includes and field not in includes:
                    continue
                elif excludes and field in excludes:
                    continue

                data = getattr(self, field)
                relout = None

                if relation.uselist:
                    relout = []
                    for obj in data:
                        if isinstance(obj, Serializable):
                            if relation.secondary is not None and mtm_pkonly:
                                relinfo = inspect(obj.__class__)
                                pkeys = relinfo.primary_key
                                out = []
                                for pk in pkeys:
                                    val = getattr(obj, pk.name)
                                    out.append(val)
                                relout.extend(out)
                            else:
                                relinfo = inspect(obj)
                                relfields = [k for k in relinfo.dict.keys() if
                                        not k.startswith('_')]


                                relout.append(obj.to_dict(relfields, 
                                    relationships=False,
                                    mtm_pkonly=mtm_pkonly))

                else:
                    if data and isinstance(data, Serializable):
                        relinfo = inspect(data)
                        relfields = [k for k in relinfo.dict.keys() if not
                                k.startswith('_')]
                        relout = data.to_dict(relfields, 
                                relationships=False,
                                mtm_pkonly=mtm_pkonly)

                if relout:
                    output[field] = relout

        #check for property() data-descriptors.
        #this is surprisingly non-intuitive.

        all_members = set([f for f in dir(self) if not f.startswith('_')])
        properties = all_members - set(info.attrs.keys())

        #TODO: figure out a better way to figure out which are valid attributes
        always_skip = set(['metadata', 'json_factory', 'to_dict', 'populate',
                'query', 'query_class'])

        for prop in properties:
            if prop in always_skip:
                continue
            elif includes and prop not in includes:
                continue
            elif excludes and prop in excludes:
                continue


            if hasattr(self, prop):
                output[prop] = _get_value(self, prop)



        return output


    def populate(self, data, skip_fields=None):
        '''Populate object from a dict of fields.

        *This method does not populate relationships*. It is recommended
        to override the method and handle them manually. 
        
        Values for relationship attributes can be supplied in the `data`
        parameter and will be safely ignored.

        :param data: A dict whose keys match the object attributes.
        :param skip_fields: An iterable of attributes to not set, whether they
            are in the data parameter or not.
        '''

        if skip_fields is None:
            skip_fields = []

        info = inspect(self)
        mapper = info.mapper
        for col in mapper.columns:
            if col.name in skip_fields:
                continue
            elif col.name in data:
                if isinstance(col.type, DateTime):
                    value = processors.str_to_datetime(data[col.name])
                elif isinstance(col.type, Date):
                    value = processors.str_to_date(data[col.name])
                elif isinstance(col.type, Time):
                    value = processors.str_to_time(data[col.name])

                else:
                    value = data[col.name]

                setattr(self, col.name, value)


    @classmethod
    def json_factory(cls, resultset, fields=None, relationships=True,
            mtm_pkonly=True):
        '''Create a generator to serialize a result or result set to JSON.

        This classmethod creates a generator that streams JSON data, wrapping
        the set in the pluralized name if the object is iterable (i.e. a list),
        or in the singular name if not.

        :param resultset: An iterable (e.g. list or SQLAlchemy query), or a
            single mapped instance.

        :param fields=None: Passed directly to `to_dict`
        :param relationships=True: Passed directly to `to_dict`
        :param mtm_pkonly=True: Passed directly to `to_dict`

        '''

        def generator():
            if isinstance(resultset, abc.Iterable):
                yield '{"%s": [' % cls.__plural__

                iresult = iter(resultset)
                try:
                    prev = next(iresult)

                    for row in iresult:
                        yield json.dumps(prev.to_dict(fields, relationships,
                            mtm_pkonly)) + ','
                        prev = row

                    yield json.dumps(prev.to_dict(fields, relationships, mtm_pkonly))
                except StopIteration:
                    pass
                except Exception as ex:
                    raise ex
                finally:
                    yield ']}'

            elif resultset is not None:
                yield json.dumps({cls.__single__: resultset.to_dict(fields,
                    relationships, mtm_pkonly)})
            else:
                yield json.dumps({cls.__single__: None})

        return generator
        

@event.listens_for(Serializable, 'mapper_configured', propagate=True)
def add_special_fields(mapper, cls):
    cls._define_special_fields()

