
"""
Many programs process items of some sort, and need to track their
progress. This leads to the use of many ad hoc containers, counters,
and such. It's more effort and leads to more errors than it should.
`statustrack` helps reduce effort and errors by providing a simple,
repeatable pattern.
"""

from stuf import stuf, orderedstuf
from .counterstuf import counterstuf
from .setspec import spec2list
import time, textwrap
import sys

_PY3 = sys.version_info[0] == 3
if _PY3:
    basestring = str

class Chore(stuf):
    """
    Representation of a work item. Piggybacks a simple-to-use,
    attribute-accessible kind of ``dict``.
    """

    def mark(self, status):
        self['status'] = status

def is_sequence(arg):
    """
    Is the given object a 'proper' sequence--i.e., a sequence but not a string?
    """
    return not hasattr(arg, "strip") and (hasattr(arg, "__getitem__") or
                                          hasattr(arg, "__iter__"))

def statistics(counter):
    """
    Simple statistics getter for a dict-like structure. Designed to
    collate stats for Counter, but no reason it can't be used on any dict.
    """
    stats = stuf()
    values = counter.values()
    stats.count = len(values)
    stats.sum = sum(values)
    stats.avg = stats.sum / stats.count
    stats.min = min(values)
    stats.max = max(values)
    return stats

def dict_print(d, heading=None, wrap=True, **kwargs):
    """
    Tidy printing of dictionary elements.
    """
    lines = []

    if wrap:
        initial = kwargs.setdefault('initial_indent', '')
        kwargs.setdefault('subsequent_indent', initial + '    ')

    if heading:
        lines.append(heading)
    for key, value in d.iteritems():
        item_text = "{0}: {1}".format(key, value)
        if wrap:
            lines.extend(textwrap.wrap(item_text, **kwargs))
        else:
            lines.append(item_text)
    return '\n'.join(lines)


class Chores(object):
    """
    A class that can remember the "status" or "dispostion" of each
    item in a collection of work. Any dict can do that, right? Sure. But this
    one conveniently provides a common model and
    statistics about what happened to each item.

    The status 'total' is reserved.

    NB: Assumes each item reported on is unique and hashable.
    """

    def __init__(self, data=None, name=None, status='new'):
        """
        Start a Chores collection. Optionally give a set of initial items and a
        default status (required for iteration or creating progress reports).
        """
        self._data = orderedstuf()  # core collection, indexed by item name/id
        self._added = None  # collects items added whilst looping
        if data:
            self.add(data, status=status)
        self._name = name if name is not None else hex(id(self))
        self._added = None  # null it out again - needed

    def addone(self, key, status='new', **kwargs):
        if key in self._data:
            raise KeyError('item {0!r} already contained'.format(key))
        payload = Chore(id=key, status=status)
        payload.update(kwargs)
        self._data[key] = payload

    def add(self, items, status='new', **kwargs):
        """
        Add the given items.
        """
        items = items if is_sequence(items) else [ items ]  # in case single thing added
        newkeys = []
        if hasattr(items, 'items'): # it's a mapping
            for key, value in items.items():
                kwargs['data'] = value
                self.addone(key, status=status, **kwargs)
            newkeys = items.keys()
        else:
            for key in items:
                self.addone(key, status=status, **kwargs)
            newkeys = items
        if self._added is not None:
            self._added.extend(newkeys)

    def m_of_n(self, m, n=None, template="[m/n]"):
        """
        Return progress tracking string like '[m/n]'
        """
        n = n or len(self._data)
        return template.replace('m', str(m)).replace('n', str(n))

    def mark(self, target, status):
        """
        Mark a target item (or collection of items) as having a given status.
        """
        assert status != 'total'
        if is_sequence(target):
            for key in target:
                self.mark(key, status)
        else:
            if target in self._data:
                self._data[target].status = status
            else:
                self._data[target] = Chore(id=target, status=status)

    def _target_statuses(self, status=None, exclude=None):
        """
        Return a set of desired statuses. If status is None and exclude is
        None, consider that a wildcard and return everything. If status is a
        scalar, return any items with that status. If a sequence, any items with
        any of those statuses. Exclude is the negative selector, giving a status
        or list of statues to exclude. Exclude works best when status is None,
        so excluding against the universe of all possible statuses.
        """
        excl = set()
        if status is None:
            targets = set([ item.status for item in self._data.values() ])
        elif isinstance(status, basestring):
            incl, excl = spec2list(status)
            targets = set(incl) if incl else set([ item.status for item in self._data.values() ])
            excl = set(excl)
        elif is_sequence(status):
            targets = set(status)
        else:
            raise ValueError("not sure what to do with include {0!r}".format(status))
        if exclude or excl:
            exclude = exclude or set()
            if isinstance(exclude, basestring):
                a, b = spec2list(exclude)
                exclude = set(a) | set(b) | set(excl) # dropping possible double negative
            elif is_sequence(exclude):
                exclude = set(exclude) | excl
            else:
                exclude = exclude | excl
                # raise ValueError("not sure what to do with exclude {0!r}".format(exclude))
            targets = targets - exclude
        return targets

    def marked(self, status=None, exclude=None, justkeys=True):
        """
        Return items marked with the given status. See ``_target_statuses()`` for how
        ``status`` and ``exclude`` are interpreted.
        """
        if status is None and exclude is None:
            return list(self._data.keys() if justkeys else self._data.values())
        else:
            kvpick = (lambda k,v: k) if justkeys else (lambda k,v: v)
            target = self._target_statuses(status, exclude)
            return [ kvpick(k,v) for k,v in self._data.items() if v.status in target ]

        # Could add the ability to make the status parameter be a lambda expression

    def count(self, status=None, exclude=None):
        """
        Return items marked with the given status. See ``_target_statuses()`` for how
        ``status`` and ``exclude`` are interpreted.
        """
        return len(self.marked(status, exclude))

    def tally(self):
        """
        Tallies how many of each kind of status were seen. Return a ``counterstuf``
        (attribute-accessible version of ``collections.Counter``) of how many of
        each status marking were observed.
        """
        return counterstuf([ item.status for key, item in self._data.items() ])

    def bystatus(self, justkeys=True):
        """
        Return an ordered dictionary, indexed by status. For each status
        key, the corresponding value is an ordered list of chore ids
        that have that status. Or if justkeys is False, return a list of
        full Chore obects.
        """
        result = orderedstuf()
        for s in self.statuses():
            result[s] = []
        for key, chore in self._data.items():
            payload = key if justkeys else chore
            result[chore.status].append(payload)
        return result

    def report(self, heading=None, total='processed', order=None):
        """
        Report status. Allows an optional heading. You can choose the
        word used to represent "everything" (default: "processed")
        and the ordering of values. If order is given, it's a space-separated
        list of status names.
        """
        rep = orderedstuf()
        tally = self.tally()
        rep[total] = sum(tally.values())
        ordering = order.split() if order else sorted(tally.keys())
        for name in ordering:
            rep[name] = tally[name]
        return dict_print(rep, heading=heading, initial_indent='    ')

    # would benefit from the ability to include/exclude

    def __iter__(self):
        """
        Iterate the collection of Chores, returning a key for each.
        If items are added during processing, handle them at the end
        of the loop.
        """
        keys = list(self._data.keys())
        self._added = []
        while keys:
            for key in keys:
                yield key
            # dos-y-dos, swing her 'round!
            keys = self._added
            self._added = []
        self._added = None

        raise StopIteration

    def data(self, key):
        """
        Return an attributes-exposed dict (``Chore``) that holds data for
        each item being tracked.
        """
        return self._data.setdefault(key, Chore())

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def keys(self):
        """
        Return the ids of each work item / ``Chore``.
        A list in Python 2, or a view object in Python 2.
        """
        return self._data.keys()

    def values(self):
        """
        Return ``Chore`` items.
        A list in Python 2, or a view object in Python 2.
        """
        return self._data.values()

    def items(self):
        """
        Return (key, value) tuples, where key = ``Chore`` id, value = ``Chore``.
        A list in Python 2, or a view object in Python 2.
        """
        return self._data.items()

    def __len__(self):
        return len(self._data)

    def statuses(self):
        """
        Return the unique list of status values. Implementation a little
        goofy because it tries to simulate an 'ordered set', giving statuses
        in the order seen, but with uniqueness. Thus both set and list
        mechanisms.
        """
        seen = []
        seenset = set()

        for v in self._data.values():
            status = v.status
            if status not in seenset:
                seenset.add(status)
                seen.append(status)
        return seen

    def __repr__(self):
        clsname = self.__class__.__name__
        return "{0}({1!r})".format(clsname, self._name)




    def __enter__(self):
        self.caller.begin(self.name)

    def __exit__(self, *args):
        self.caller.end(self.name)
