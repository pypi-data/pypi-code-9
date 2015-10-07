import pdb
import difflib, json, time, types, uuid
from difflib import SequenceMatcher

""" Brine is a play on Python's pickle module, which is used for
    serializing data. Brine is used for serialization as well, but
    into JSON, not a binary structure.
"""

# Declare a set of method types that should be filtered for.
METHOD_TYPES = [types.MethodType, types.FunctionType, types.LambdaType]


def fuzzy_ratio(a, b):
    """ Compares two values using the SequenceMatcher from difflib.
        Used for ~approximated~ fuzzy search.
    """

    return SequenceMatcher(None, a, b).ratio()


class BrineObject(object):
    """ This object is for use as a base class for other data.
        Essentially, it will expose a set of members that can be set
        and then squashed down to a JSON object through a call to to_json.

        It can also be used as a meta-class for the base of a caching object
        model or other neat things.
    """

    def __init__(self, *args, **kw):

        # Do this because MRO.
        super(BrineObject, self).__init__()

        # For now, lets make this simple and treat fields with no special
        # syntax (underlines, mainly) as our schema.
        self._special_fields = ["timestamp", "uuid"]
        self._fields = []
        for field in dir(self):
            if field.startswith("_"):
                continue
            # Also, make sure this isn't a function.
            if type(getattr(self, field)) in METHOD_TYPES:
                continue
            self._fields.append(field)

        if kw.get("timestamp", False):
            self.timestamp = int(time.time())

        if kw.get("uuid", False):
            self.uuid = str(uuid.uuid4())

    def as_dict(self):
        """ Returns the dictionary representation of the fields
            in this object.
        """

        obj = {}

        for val in self._fields + self._special_fields:
            if not hasattr(self, val):
                continue
            # Also, make sure this isn't a function.
            if type(getattr(self, val)) in METHOD_TYPES:
                continue
            obj.update({val: getattr(self, val)})

        return obj

    def to_json(self):
        """ Converts the object into JSON form.
            Simple, right?
        """

        return json.dumps(self.as_dict())

    def from_json(self, data):
        """ Converts the JSON data back into an object, then loads
            the data into the model instance.
        """

        obj = json.loads(data)

        if not isinstance(obj, dict):
            raise TypeError("Expected JSON serialized dictionary, not %s" % (
                type(obj)))

        for k, v in obj.iteritems():
            # We need to make sure the data is sanitized a little bit.
            if k.startswith("_") and k not in self._special_fields:
                continue
            if k in self._fields:
                setattr(self, k, v)


class CachingBrineObject(BrineObject):
    """ This is a magical class that performs the same function as the
        BrineObject, but it also adds object caching, searching, and fuzzy
        searching on the cache. Also provided is cached field invalidation /
        "dirtying".
    """

    # Ratio for fuzzy search. Closer to 1.0 means stricter results.
    _FUZZ_RATIO = 0.535

    @classmethod
    def __initialize_cache(cls):
        """ Initialize a class-level cache to store Json models for cache and
            searching purposes.
        """

        if not hasattr(cls, "_CachingBrineObject__cache"):
            cls.__cache = []

    @classmethod
    def fuzzy_search(cls, ignore_case = False, **kw):
        """ Performs a fuzzy search on the cache to find objects that have at
            least a diff ratio of FUZZ_RATIO.

            Note that this can return more than one object and it may not be
            accurate. Time will tell.

            Returns a list of matches ordered by likelihood of match.
        """

        ratios = {}

        for k, v in kw.iteritems():
            for obj in cls.__cache:
                ob_value = getattr(obj, k, None)
                if ignore_case:
                    if isinstance(v, str) and isinstance(ob_value, str):
                        r = fuzzy_ratio(ob_value.lower(), v.lower())
                else:
                    r = fuzzy_ratio(ob_value, v)
                if r >= cls._FUZZ_RATIO:
                    ratios.update({obj: r})

        # TODO - sort by fuzzy search ratio.
        # We need to ensure the results get properly sorted by match ratio
        # before returning.

        return ratios.keys()

    @classmethod
    def search(cls, ignore_case = False, **kw):
        """ Searches through the cache to find objects with field that match
            those given by the **kw.

            Note that this can return more than one object.
        """

        result = []

        for k, v in kw.iteritems():
            for obj in cls.__cache:
                ob_value = getattr(obj, k, None)
                if ignore_case:
                    if isinstance(v, str) and isinstance(ob_value, str):
                        r = (v.lower() == ob_value.lower())
                else:
                    r = (v == ob_value)
                if r:
                    if obj in result:
                        continue
                    else:
                        result.append(obj)
                else:
                    continue

        return result

    def __init__(self, *args, **kw):

        # Call the parent initializer.
        super(CachingBrineObject, self).__init__(self, *args, **kw)
        self._initialized = False

        # Make sure the cache is initialized.
        self.__initialize_cache()

        # The "dirty" cache list is just a list of fields that have been
        # updated.
        self.__dirty = []

        # Throw this object into the cache.
        self.__cache.append(self)

        # Let the attribute handler know we're done loading.
        self._initialized = True

    def __setattr__(self, attr, value):
        """ Sets local fields and determines if the cache needs to be
            marked dirty for that set and ensures that the value can
            actually be set.
        """

        # I wish this didn't have to be a special case.
        if attr == "_initialized":
            self.__dict__[attr] = value
            return

        # Check that init has finished.
        if not getattr(self, "_initialized", False):
            self.__dict__[attr] = value
            return

        # Check various conditions used to determine if a variable has been
        # dirtied or can be set.
        if attr in self._fields:
            if attr not in self.__dirty:
                self.__dirty.append(attr)
        elif attr in self._special_fields:
            raise AttributeError("Special field {} is immutable.".format(attr))
        elif attr not in self.__dict__:
            raise AttributeError("Field {} does not exist.".format(attr))

        # Verify that the set *will not* overwrite a method.
        _attr_cur = getattr(self, attr)
        if type(_attr_cur) in METHOD_TYPES:
            raise TypeError("Function {} can not be overwritten.".format(attr))

        # Set the variable in the dictionary.
        self.__dict__[attr] = value

    def uncache(self):
        """ Removes the object from the state cache forcibly.
        """

        self.__cache.remove(self)

    def unmark(self, *fields):
        """ Unmarks some field as dirty. Should only be called after
            the upstream is updated or only if you know what you're doing!
        """

        for field in fields:
            if field not in self.__dirty:
                continue

            self.__dirty.remove(field)

    def dirty_dict(self):
        """ Dumps a dictionary of dirty fields.
        """

        obj = {}
        for val in self.__dirty:
            if not hasattr(self, val):
                continue
            # Also, make sure this isn't a function.
            if type(getattr(self, val)) in METHOD_TYPES:
                continue
            obj.update({val: getattr(self, val)})

        return obj

    def dirty_json(self):
        """ Dumps the dirty dictionary as JSON.
        """

        return json.dumps(self.dirty_dict())

