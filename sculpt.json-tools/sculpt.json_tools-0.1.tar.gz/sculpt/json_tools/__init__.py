try:
    from django.db.models.manager import QuerySet
except ImportError:
    class QuerySet(object):
        pass
import datetime
import numbers
import types

# JSON tools

# to_json
#
# Various complex data structures often need to be rendered
# as JSON-compatible data. In some ways this is simpler to do
# than trying to extend the JSON encoding classes, especially
# in cases where access to the JSON codec is difficult. Yet
# we still need to provide a way to control the output of
# data.
#
# This function "sanitizes" data and makes it JSON safe.
# Scalars are accepted rather directly, as are lists; tuples
# are converted to lists at this stage (but the JSON serializer
# would have done that anyway) and Django QuerySet objects
# are treated as lists and thus evaluated here.
#
# Dicts and objects are both rendered as dicts, but with
# slight differences. For dicts, by default all keys are
# processed and included, but an optional attrlist may be
# provided which limits the extraction to just those keys.
# For objects, the attrlist is REQUIRED. The attrlist is
# expected to contain a list of keys/attributes to be
# extracted but an item may instead be a callable; this
# callable should return a (k,v) tuple that will be used
# as the key and value in the output dict. The attrlist
# may also contain explicit (k,v) tuples which will be
# included in the output directly, subject to v being
# properly processed.
#
# to_json is a recursive function. Elements in lists, dicts,
# or objects are serialized by nested calls to to_json.
# This presents a problem when objects are contained within
# other objects, as serializing an object REQUIRES an
# explicit attrlist (as a safety measure). To facilitate
# this, when a nested object is about to be serialized,
# if it contains a to_json method, that method will be
# invoked rather than the core to_json function. Many
# implementations of to_json on classes simply invoke the
# core to_json method with an explicit list of approved
# attributes for serialization.
#
# to_json accepts arbitrary parameters, but only processes
# one (see typemap, below), All other parameters are passed
# unchanged to nested calls and are also passed to any
# to_json methods, which is the primary reason for using
# these extra parameters: they allow you to provide some
# context to an object to help it know how it should render
# itself. Exactly what parameters you should use are
# entirely up to you. Note that when attrlist includes
# callables, additional to_json parameters are ALSO passed
# to those callables, so your callables must accept **kwargs
# and ignore them if they do not use them.
#
# Sometimes you need to work with classes you cannot extend
# or practically replace, yet still serialize them to JSON
# in a controlled fashion. You may pass a typemap parameter
# to do this. typemap is a dict. Its keys may be either
# strings (which should be class names) or actual type
# objects. The values may be type objects or callables.
# If the value is a type object, the object will be treated
# as though it had that class (a duck typing hint). If the
# value is a callable, it will be called with the object
# and it may return a directly-usable object (scalar, list,
# dict, object) OR it may return a tuple of attributes,
# in which case the object will be processed as an object
# with the given attrlist.
#
# NOTE: some of the tweaks are to accomodate C#, since the
# original code was developed for Innovative Leisure and their
# Unity C# projects; some additional quirks are to accommodate
# Jython, since a few of the native Python types (int, long,
# float, I'm looking at you) do not have a usable common base
# class to test for.
#
def to_json(obj, attrlist = None, **kwargs):

    # determine the class and the class name of this object
    # (because we might treat it as something different than
    # it is, if we have a user-supplied typemap)
    obj_class = obj.__class__
    if 'typemap' in kwargs:
        # we have a typemap; see if this object's class is in it
        typemap = kwargs['typemap']
        obj_class_translated = None
        if obj_class in typemap:
            obj_class_translated = typemap[obj_class]
        elif obj_class.__name__ in typemap:
            obj_class_translated = typemap[obj_class.__name__]
            
        # if we actually got a translated class, check to see
        # whether it's a function or just a new type
        if isinstance(obj_class_translated, types.FunctionType):
            # this is a callable function (can't use callable()
            # because classes are callable)
            translated = obj_class_translated(obj, attrlist, **kwargs)
            
            if isinstance(translated, tuple):
                # we got back a new attribute list; this overrides
                # any explicit attribute list given to us
                attrlist = translated
                
            else:
                # we got back a fully-translated, sanitized blob;
                # stop processing it
                return translated
    
        elif obj_class_translated != None:
            # otherwise, since we don't have a function, we should
            # have a class; treat the current object as though it
            # is that class
            obj_class = obj_class_translated
        
    if issubclass(obj_class, datetime.datetime):
        # Tricky bit: .isoformat() will include a time zone
        # offset if one is known, even if that time zone is
        # UTC (this is rational). However, C# doesn't have
        # a format that conditionally accepts this, so we
        # define our API as always passing UTC and we strip
        # any timezone from the result if one is provided
        #print "[pid:%d]" % os.getpid(), 'datetime'
        return obj.isoformat()[:19]

    elif issubclass(obj_class, (str, unicode, numbers.Number, types.NoneType)) or obj_class.__name__ in [ 'int', 'long', 'float' ]:
        # "scalar" type, can be converted to a single JSON element
        # (no conversion required)
        #print "[pid:%d]" % os.getpid(), 'direct type', obj.__class__.__name__
        return obj
        
    elif issubclass(obj_class, (list, QuerySet, tuple)) or obj_class.__name__ == 'ArrayList':
        # given a bare list or QuerySet; JSONify each element
        # NOTE: callables are NOT supported since they return (k,v)
        # and we don't use keys in lists
        #print "[pid:%d]" % os.getpid(), 'list type', obj.__class__.__name__, repr(obj)
        d = []
        for o in obj:
            if hasattr(o, 'to_json'):
                d.append(o.to_json(**kwargs))   # object knows how to serialize itself
            else:
                d.append(to_json(o, **kwargs))  # hope that it can be serialized automatically
            
        return d
    
    elif issubclass(obj_class, dict) or obj_class.__name__ == 'HashMap':
        # a dict; process all the elements to JSONify them
        # (we do not assume they are already JSON-ready)
        #print "[pid:%d]" % os.getpid(), 'dict type', obj.__class__.__name__, repr(obj)
        d = {}
        if attrlist == None:
            if obj_class.__name__ == 'HashMap':
                attrlist = obj.keySet() # Java HashMap gives us this function to get keys
            else:
                attrlist = obj.keys()   # attrlist is optional for dicts and defaults to all of it
        for a in attrlist:
            if callable(a):
                #print "[pid:%d]" % os.getpid(), 'fn:', a.__name__
                a, v = a(obj, **kwargs) # get key, value pair from a function
            elif isinstance(a, tuple):
                #print "[pid:%d]" % os.getpid(), 'tuple:', a.__name__
                a, v = a                # use the provided value rather than looking it up by name
            else:
                #print "[pid:%d]" % os.getpid(), 'attr:', repr(a)
                v = obj[a]              # have key, get value (and raise KeyError if missing)
    
            #print "[pid:%d]" % os.getpid(), 'value:', v.__class__.__name__, repr(v)
            if hasattr(v, 'to_json'):
                d[a] = v.to_json(**kwargs)
            else:
                # something else; recursively JSONify it
                # NOTE: this is a bit of a performance hit and it
                # creates copies of all the nested data, even if
                # they are already in JSON-compatible form, but
                # it makes it MUCH easier to convert data coming
                # out of Django QuerySets
                d[a] = to_json(v, **kwargs)

        return d

    else:
        # an object; convert to a dict that can be JSON-serialized
        d = {}
        if attrlist == None:
            raise Exception('attrlist cannot be none for objects of type ' + obj.__class__.__name__)
        for a in attrlist:
            if callable(a):
                #print "[pid:%d]" % os.getpid(), 'fn:', a.__name__
                a, v = a(obj, **kwargs) # get key, value pair from a function
            elif isinstance(a, tuple):
                #print "[pid:%d]" % os.getpid(), 'tuple:', a.__name__
                a, v = a                # use the provided value rather than looking it up by name
            else:
                #print "[pid:%d]" % os.getpid(), 'attr:', repr(a)
                v = getattr(obj, a)     # have key, get value (and raise AttributeError if missing)

            #print "[pid:%d]" % os.getpid(), 'value:', v.__class__.__name__, repr(v)
            if hasattr(v, 'to_json'):
                d[a] = v.to_json(**kwargs)
            else:
                # something else; recursively JSONify it
                # NOTE: this is a bit of a performance hit and it
                # creates copies of all the nested data, even if
                # they are already in JSON-compatible form, but
                # it makes it MUCH easier to convert data coming
                # out of Django QuerySets
                d[a] = to_json(v, **kwargs)

        return d

# extract from JSON
#
# Often when working with JSON data fetched from outside
# sources, we need to quickly look for a deeply-nested
# element and extract it if it's available or return None
# if it's missing. We need to check at each level of the
# nested structure if the next step is available.
#
# This is a wrapper around extract_default, because Python's
# rules for assigning parameters will fill in the default
# with the first entry from *args if it's missing, which is
# not what we want.
#
def extract(obj, *args):
    return extract_default(obj, None, *args)

# Same as above, except this time we can provide a default
# value to use if the requested item can't be found (no
# matter where in the path it fails). This is similar to
# Python's .get() method for dicts. Note that with this
# method, default must be specified; ø
#
def extract_default(obj, default, *args):
    for a in args:
        if isinstance(obj, list):
            # should be a numeric index
            if a >= 0 and a < len(obj):
                obj = obj[a]
            else:
                return default

        elif isinstance(obj, dict):
            # could be any kind of key
            if a in obj:
                obj = obj[a]
            else:
                return default

        else:
            # some other type we can't look into;
            # fail (but quietly)
            # THIS IS A DESIGN CHOICE. We could raise
            # an exception instead.
            return default

    return obj

# useful conversion edge case handlers

# empty_if_none
# returns the original string, or '' if it's None
# (this is useful shorthand when s is a complicated expression)
def empty_if_none(s):
    return s if s != None else ''

# given a particular string, attempt to parse it as an
# ISO-format datetime and return that; return None if
# not valid
def parse_datetime(v):
    try:
        return datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        return None

