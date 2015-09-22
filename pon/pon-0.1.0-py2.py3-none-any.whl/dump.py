# coding: utf-8

import sys as _sys
import warnings

from pon import ordereddict, string_type


# try:
#     from cStringIO import StringIO as _StringIO
# except ImportError:
#     from io import StringIO as _StringIO
from io import StringIO as _StringIO

__all__ = ["PrettyPrinter"]

# cache these for faster access:
_commajoin = ", ".join
_id = id
_len = len
_type = type


def _sorted(iterable):
    with warnings.catch_warnings():
        if hasattr(_sys, 'py3kwarning') and _sys.py3kwarning:
            warnings.filterwarnings("ignore", "comparing unequal types "
                                    "not supported", DeprecationWarning)
        return sorted(iterable)


class PrettyPrinter:
    def __init__(self, indent=4, width=80, depth=None, stream=None, rt_info=None):
        """Handle pretty printing operations onto a stream using a set of
        configured parameters.

        indent
            Number of spaces to indent for each level of nesting.

        width
            Attempted maximum number of columns in the output.

        depth
            The maximum depth to print out nested structures.

        stream
            The desired output stream.  If omitted (or false), the standard
            output stream available at construction will be used.

        """
        indent = int(indent)
        width = int(width)
        assert indent >= 0, "indent must be >= 0"
        assert depth is None or depth > 0, "depth must be > 0"
        assert width, "width must be != 0"
        self._depth = depth
        self._indent_per_level = indent
        self._width = width
        if stream is not None:
            self._stream = stream
        else:
            self._stream = _sys.stdout
        self._rt_info = rt_info
        self._prefix = []
        self._eol = None
        self._col = 0

    def _add_key(self, key):
        self._prefix.append(key)

    def _pop_key(self):
        self._prefix.pop()

    def write(self, s, stream=None):
        if stream is None:
            stream = self._stream
        for ch in s:
            if ch == '\n':
                self._col = 0
                if self._eol:
                    stream.write(self._eol)
                    self._eol = None
                stream.write(ch)
                continue
            stream.write(ch)
            self._col += 1

    def decode_write(self, s, stream=None):
        if _sys.version_info < (3, ) and isinstance(s, str):
            s = s.decode('utf-8')
        self.write(s, stream=stream)

    def pprint(self, object):
        for c in self._rt_info[0]:
            self.write(u"{0}{1}\n".format(' ' * c[2], c[0]))
        self._format(object, self._stream, 0, 0, {}, 0)
        self.write(u"\n")
        for c in self._rt_info[3]:
            self.write(u"{0}{1}\n".format(' ' * c[2], c[0]))

    def pformat(self, object):
        sio = _StringIO()
        self._format(object, sio, 0, 0, {}, 0)
        return sio.getvalue()

    def indent(self, level):
        return u' ' * self._indent_per_level * level

    def _format(self, object, stream, indent, allowance, context, level):
        level = level + 1
        objid = _id(object)
        if objid in context:
            stream.write(_recursion(object))
            self._recursive = True
            self._readable = False
            return
        rep = self._repr(object, context, level - 1)
        typ = _type(object)
        sepLines = _len(rep) > (self._width - 1 - indent - allowance)
        write = self.write

        if self._depth and level > self._depth:
            write(rep)
            return

        r = getattr(typ, "__repr__", None)
        # print(type(object), typ == ordereddict, issubclass(typ, dict),
        #       r, ordereddict.__repr__)
        if issubclass(typ, dict) and \
           (r is dict.__repr__ or r == ordereddict.__repr__):
            if not self._prefix:
                curly_braces = self._rt_info[4]
                sepLines = True
            else:
                curly_braces = self._rt_info[1][tuple(self._prefix)][2] == -2
                sepLines = not curly_braces
            if curly_braces:
                write(u'{')
                # if self._indent_per_level > 1:
                #     write((self._indent_per_level - 1) * ' ')
                length = _len(object)
                if length:
                    context[objid] = 1
                    if sepLines:
                        indent += 1
                        write(u'\n%s' % (self.indent(indent)))
                    items = list(object.items())
                    key, ent = items[0]
                    self._add_key(key)
                    rep = self._repr(key, context, level)
                    self.decode_write(rep)
                    write(u': ')
                    self._format(ent, stream, indent + _len(rep) + 2,
                                 allowance + 1, context, level)
                    self._pop_key()
                    if length > 1:
                        for key, ent in items[1:]:
                            self._add_key(key)
                            rep = self._repr(key, context, level)
                            pre, eol = self._rt_info[1][tuple(self._prefix)][3:5]
                            for c in pre:
                                write(u"{0}{1}\n".format(' ' * c[2], c[0]))
                            if sepLines:
                                write(u',\n%s%s: ' % (self.indent(indent), rep))
                            else:
                                write(u', %s: ' % rep)
                            if eol:
                                self._eol = "{0}{1}".format(' ' * (eol[2] - eol[3]), eol[0])
                            self._format(ent, stream, indent + _len(rep) + 2,
                                         allowance + 1, context, level)
                            self._pop_key()
                    if sepLines:
                        indent -= 1
                    del context[objid]
                if sepLines:
                    write(u',\n%s' % (self.indent(indent)))
                write(u'}')
                return
            else:
                write(u'dict(')
                length = _len(object)
                if length:
                    write(u'\n')
                    context[objid] = 1
                    indent += 1
                    items = object.items()
                    for key, ent in items:
                        rep = key
                        self._add_key(key)
                        pre, eol = self._rt_info[1][tuple(self._prefix)][3:5]
                        for c in pre:
                            write(u"{0}{1}\n".format(' ' * c[2], c[0]))
                        if eol:
                            self._eol = u"{0}{1}".format(' ' * (eol[2] - eol[3]), eol[0])
                        if sepLines:
                            write(u'%s%s=' % (self.indent(indent), rep))
                        else:
                            write(u'%s=' % rep)
                        self._format(ent, stream, indent,
                                     allowance + 1, context, level)
                        self._pop_key()
                        write(u',\n')
                    indent -= 1
                    del context[objid]
                if not self._prefix:
                    for c in self._rt_info[2]:
                        write(u"{0}{1}\n".format(' ' * c[2], c[0]))
                write(u"%s%s" % (self.indent(indent), ')'))
                return

        if ((issubclass(typ, list) and r is list.__repr__) or
           (issubclass(typ, tuple) and r is tuple.__repr__) or
           (issubclass(typ, set) and r is set.__repr__) or
           (issubclass(typ, frozenset) and r is frozenset.__repr__)):
            length = _len(object)
            if issubclass(typ, list):
                write(u'[')
                endchar = ']'
            elif issubclass(typ, tuple):
                write(u'(')
                endchar = ')'
            else:
                if not length:
                    write(rep)
                    return
                self.decode_write(typ.__name__)
                write(u'([')
                endchar = '])'
                # indent += len(typ.__name__) + 1
                object = _sorted(object)
            end_sep = sepLines
            # if self._indent_per_level > 1 and sepLines:
            #     write((self._indent_per_level - 1) * ' ')
            idx = -1
            if length:
                same_line = self._rt_info[1][tuple(self._prefix)][0]
                context[objid] = 1
                if sepLines:
                    indent += 1
                # self._add_key(idx)
                #  self._format(object[0], stream, indent, allowance + 1,
                #              context, level)
                # self._pop_key()
                if length > 0:
                    for ent in object:
                        idx += 1
                        self._add_key(idx)
                        if issubclass(typ, list):
                            my_line = self._rt_info[1][tuple(self._prefix)][0]

                            sep_lines = my_line != same_line
                            same_line == my_line
                            end_sep = sep_lines
                        else:
                            sep_lines = sepLines
                        if idx:
                            if sep_lines:
                                write(u',\n')
                            else:
                                write(u', ')
                        else:  # first element
                            if sep_lines:
                                write(u'\n')
                        if issubclass(typ, list):
                            pre, eol = self._rt_info[1][tuple(self._prefix)][3:5]
                            for c in pre:
                                write(u"{0}{1}\n".format(' ' * c[2], c[0]))
                            if eol:
                                self._eol = "{0}{1}".format(' ' * (eol[2] - eol[3]), eol[0])
                        if sep_lines:
                            self.write(self.indent(indent))
                        self._format(ent, stream, indent,
                                     allowance + 1, context, level)
                        self._pop_key()
                if sepLines:
                    indent -= 1
                del context[objid]
            if issubclass(typ, tuple) and length == 1:
                write(u',')
            if end_sep:
                write(u",\n%s%s" % (self.indent(indent), endchar))
            else:
                write(u"%s" % endchar)
            return
        if rep.startswith('datetime.date'):
            rep = rep.replace('datetime.date', 'date', 1)
            self.decode_write(rep)
            return
        if isinstance(rep, string_type):
            self.decode_write(rep)
            return
        print('unknown typ:', rep)
        raise NotImplementedError

    def _repr(self, object, context, level):
        repr1, readable, recursive = self.format(object, context.copy(),
                                                 self._depth, level)
        if not readable:
            self._readable = False
        if recursive:
            self._recursive = True
        return repr1

    def format(self, object, context, maxlevels, level):
        """Format object for a specific context, returning a string
        and flags indicating whether the representation is 'readable'
        and whether the object represents a recursive construct.
        """
        return self._safe_repr(object, context, maxlevels, level)

    # Return triple (repr_string, isreadable, isrecursive).

    def _safe_repr(self, object, context, maxlevels, level):
        typ = _type(object)
        if typ is str:
            str_typ = self._rt_info[1][tuple(self._prefix)][2]
            # if str_typ not in [-1, -3] and 'locale' not in _sys.modules:
            #     rep = repr(object)
            #     if _sys.version_info < (3, 0):
            #         rep = rep.decode('utf-8')
            #     print('safe', typ, object)
            #     return rep, True, False
            pref = u''
            if str_typ in [-1, -3]:  # mls, dedented
                quotes = {'\n': '\n'}
            elif "'" in object and '"' not in object:
                closure = '"'
                quotes = {'"': '\\"'}
            else:
                closure = "'"
                quotes = {"'": "\\'"}
            qget = quotes.get
            sio = _StringIO()
            for char in object:
                if char.isalpha():
                    self.decode_write(char, stream=sio)
                    if _sys.version_info >= (3, ) and ord(char) > 255:
                        pref = u'u'
                else:
                    self.decode_write(qget(char, repr(char)[1:-1]), stream=sio)
            if str_typ == -3:  # dedented
                s = sio.getvalue().split('\n')
                s = (u'\n' + self.indent(level + 1)).join(s[:-1]) + \
                    u'\n' + self.indent(level) + s[-1]
                return (u'dedent("""%s""")' % (s)), True, False
            elif str_typ == -1:
                s = sio.getvalue()
                return (u'"""%s"""' % (s)), True, False
            return (u"%s%s%s%s" % (pref, closure, sio.getvalue(), closure)), True, False

        r = getattr(typ, "__repr__", None)
        if issubclass(typ, dict) and r is dict.__repr__:
            if not object:
                return u"{}", True, False
            objid = _id(object)
            if maxlevels and level >= maxlevels:
                return u"{...}", False, objid in context
            if objid in context:
                return _recursion(object), False, True
            context[objid] = 1
            readable = True
            recursive = False
            components = []
            append = components.append
            level += 1
            for k, v in object.items():
                krepr, kreadable, krecur = self._saferepr(k, context, maxlevels, level)
                vrepr, vreadable, vrecur = self._saferepr(v, context, maxlevels, level)
                append("%s: %s" % (krepr, vrepr))
                readable = readable and kreadable and vreadable
                if krecur or vrecur:
                    recursive = True
            del context[objid]
            return u"{%s}" % _commajoin(components), readable, recursive

        if (issubclass(typ, list) and r is list.__repr__) or \
           (issubclass(typ, tuple) and r is tuple.__repr__):
            if issubclass(typ, list):
                if not object:
                    return "[]", True, False
                format = u"[%s]"
            elif _len(object) == 1:
                format = u"(%s,)"
            else:
                if not object:
                    return u"()", True, False
                format = u"(%s)"
            objid = _id(object)
            if maxlevels and level >= maxlevels:
                return format % u"...", False, objid in context
            if objid in context:
                return _recursion(object), False, True
            context[objid] = 1
            readable = True
            recursive = False
            components = []
            append = components.append
            level += 1
            for o in object:
                orepr, oreadable, orecur = self._safe_repr(o, context, maxlevels, level)
                append(orepr)
                if not oreadable:
                    readable = False
                if orecur:
                    recursive = True
            del context[objid]
            return format % _commajoin(components), readable, recursive

        if _sys.version_info < (3,) and issubclass(typ, unicode):
            rep = u"u'{0}'".format(object)
        else:
            rep = repr(object)
        return rep, (rep and not rep.startswith(u'<')), False


def _recursion(object):
    return ("<Recursion on %s with id=%s>"
            % (_type(object).__name__, _id(object)))
