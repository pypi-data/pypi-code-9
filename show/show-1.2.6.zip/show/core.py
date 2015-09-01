"""Debugging print features. """

import inspect
import sys
import os
import re
import six
import fnmatch
import pprint
from options import Options, OptionsClass, OptionsContext, Transient
from say import Fmt, fmt, say
from say.core import Say, SayReturn
from .linecacher import *
from .introspect import *
from .util import *
from .exceptions import *
from .version import __version__
from functools import wraps

from nulltype import NullType
Private    = NullType('Private')
Impossible = NullType('Impossible')
Ignore     = NullType('Ignore')

_PY3 = sys.version_info[0] > 2
DEBUGGING = True

CallArgs.add_target_func('show')


QUOTE_CHARS = ('"', "'", '"""', "'''")


# probably cannot make this work from interactive Python
# http://stackoverflow.com/questions/13204161/how-to-access-the-calling-source-line-from-interactive-shell


def _afunction(f): pass
function = type(_afunction)
module   = type(sys)
class _XYZ(object):
    def method(self): pass
_xyz = _XYZ()

if _PY3:
    unicode = str
    basestring = str

FUNKY = (function, module, type, type(_XYZ.method), type(_xyz.method), type(len)) # funky => functional infrastructure


def methset(cls, mname, **kwargs):
    """
    Called to update a method's default args
    """
    # print "methset: cls:", cls, "mname:", mname
    methdefs = cls.meth_defaults.setdefault(mname, {})
    methdefs.update(kwargs)


def install_method_setter(cls, mname):
    meth = getattr(cls, mname)
    target = meth if _PY3 else meth.__func__
    setattr(target, 'set', lambda **kwargs: methset(cls, mname, **kwargs))


def install_method_setters(cls, methnames):
    """
    Called once class is defined to update those methods
    that need to have per-method set() routines
    """
    if isinstance(methnames, basestring):
        methnames = methnames.strip().split()
    for mname in methnames:
        meth = getattr(cls, mname)
        # print "mname:", mname, "meth:", meth

        target = meth if _PY3 else meth.__func__
        setattr(target, 'set', lambda **kwargs: methset(cls, mname, **kwargs))

    # TODO: clean this up by integrating with @methargs decorator
    # Does not seem to work to do them all in one process -- which is
    # perplexing, but probably due to some subtle closure / context locking


class Show(OptionsClass):

    """
    Show objects print debug output in a 'name: value' format that
    is convenient for discovering what's going on as a program runs.
    """

    options = Options(
        show_module=False,  # Show the module name in the call location
        where=False,        # show the call location of each call
        sep="  ",           # separate items with two spaces, by default
        retvalue=False,     # return the value printed?
        props=Transient,    # props desired to print (given at call time)
        omit=Transient,     # vars not to print (for those like show.locals,
                            # show.dir, etc that might default to many)
        fmtfunc=repr,       # formatting func used to format each value
        fmtcode=unicode,    # formatting used to format code snippets
        show=True,          # show or not
    )

    meth_defaults = {}

    def __init__(self, **kwargs):
        self.options = self.opts = Show.options.push(kwargs)
        self.fmt = Fmt()
        self.say = SayReturn()
        self._watching = {} # remembers last value of variables for given frames
        self.__version__ = __version__


    def call_location(self, caller):
        """
        Create a call location string indicating where a show() was called.
        """
        if isInteractive:
            return "<stdin>:{0}".format(len(history.lines))
        else:
            module_name = ""
            if self.opts.show_module:
                filepath = caller.f_locals.get('__file__', caller.f_globals.get('__file__', 'UNKNOWN'))
                filename = os.path.basename(filepath)
                module_name = re.sub(r'.py', '', filename)

            lineno = caller.f_lineno
            co_name = caller.f_code.co_name
            if co_name == '<module>':
                co_name = '__main__'
            func_location = wrapped_if(module_name, ":") + wrapped_if(co_name, "", "()")
            return ':'.join([func_location, str(lineno)])

    def value_repr(self, value):
        """
        Return a ``repr()`` string for value that has any brace characters (e.g.
        for ``dict``--and in Python 3, ``set`--literals) doubled so that they
        are not interpreted as format template characters when the composed string
        is eventually output by ``say``.
        """
        return self.fmt.escape(self.opts.fmtfunc(value))

    def code_repr(self, code):
        """
        Return a formatted string for code. If there are any internal brace
        characters, they are doubled so that they are not interpreted as format
        template characters when the composed string is eventually output by
        ``say``.
        """
        return self.fmt.escape(self.opts.fmtcode(code))

    def arg_format(self, name, value, caller, opts):
        """
        Format a single argument. Strings returned formatted.
        """
        if name.startswith(QUOTE_CHARS):
            return fmt(value, **{'_callframe': caller})
        else:
            return ': '.join( [ name, self.value_repr(value) ] )

    def arg_format_items(self, name, value, caller, opts):
        """
        Format a single argument to show items of a collection.
        """
        if name.startswith(QUOTE_CHARS):
            ret = fmt(value, **{'_callframe': caller})
            return ret
        else:
            fvalue = self.value_repr(value)
            if isinstance(value, (list, dict, set, basestring)):  # weak test
                length = len(value)
                itemname = 'char' if isinstance(value, basestring) else 'item'
                s_or_nothing = '' if length == 1 else 's'
                return "{0} ({1} {2}{3}): {4}".format(name, length, itemname, s_or_nothing, fvalue)
            else:
                return "{0}: {1}".format(name, fvalue)

    def arg_format_dir(self, name, value, caller, opts):
        """
        Format a single argument to show items of a collection.
        """
        if name.startswith(QUOTE_CHARS):
            ret = fmt(value, **{'_callframe': caller})
            return ret
        else:
            attnames = omitnames(dir(value), opts.omit)
            return "{0}{1}: {2}".format(name, typename(value), ' '.join(attnames))

    def arg_format_props(self, name, value, caller, opts, ignore_funky=True):
        """
        Format a single argument to show properties.
        """
        if name.startswith(QUOTE_CHARS):
            ret = fmt(value, **{'_callframe': caller})
            return ret
        else:
            try:
                props = self.opts.props
                if props and isinstance(props, basestr):
                    proplist = props.split(',') if ',' in props else props.split()
                    proplist = [ p.strip() for p in proplist ]
                else:
                    propkeys = object_props(value)
                    if opts.omit:
                        propkeys = omitnames(propkeys, opts.omit)
                    if ignore_funky:
                        propkeys = [ p for p in propkeys if not isinstance(getattr(value, p), FUNKY) ]

                    proplist = sorted(propkeys, key=lambda x: x.replace('_','~'))
                #propvals = [ "{0}={1}".format(p, self.value_repr(getattr(value, p))) for p in proplist ]
                #return "{0}: {1}".format(name, ' '.join(propvals))
                propvals = [ "    {0}={1}".format(p, ellipsis(self.value_repr(getattr(value, p)))) for p in proplist ]

                # change out brace charactes likely to cause problems
                LUBRACE, RUBRACE = six.u("\u2774"), six.u("\u2775")
                propvals = [ p.replace("{{", LUBRACE).replace("}}", RUBRACE) for p in propvals ]
                # this is probably totally broken

                if hasattr(value, 'items'):
                    propvals += [ "    {0}: {1}".format(k, ellipsis(self.value_repr(v))) for k,v in value.items() ]
                    fpropvals = "{0}{1}:\n{2}".format(name, typename(value), '\n'.join(propvals))
                    return fpropvals
                else:
                    fpropvals =  "{0}{1}:\n{2}".format(name, typename(value), '\n'.join(propvals))
                    return fpropvals
            except Exception as e:
                return "{0}{1}: {2}".format(name, typename(value), self.value_repr(value))

    def get_arg_tuples(self, caller, values):
        """
        Return a list of argument (name, value) tuples.
        :caller: The calling frame.
        :values: The with the given values.
        """
        filename, lineno = frame_to_source_info(caller)
        try:
            argnames = CallArgs(filename, lineno).args
        except ArgsUnavailable:
            argnames = None
        if argnames is None:
            argnames = ['?'] * len(values)
        return list(zip(argnames, list(values)))


    def set(self, **kwargs):
        """
        Change the values of the show.
        """
        self.options.set(**kwargs)
        self.fmt.set(**kwargs)
        self.say.set(**kwargs)

        # TODO: HMMM - do we need combo say/fmt feature from say after all?

        # NB this is the paradigm usage of ``options``'s "leftovers" strategy

    def clone(self, **kwargs):
        """
        Create a child instance whose options are chained to this instance's
        options (and thence to Show.options). kwargs become the child instance's
        overlay options. Because of how the source code is parsed, clones must
        be named via simple assignment.
        """
        child = Show()
        child.options = self.options.push(kwargs)

        # introspect caller to find what is being assigned to
        caller = inspect.currentframe().f_back
        filename, lineno = frame_to_source_info(caller)
        name = getline(filename, lineno).strip().split()[0]
        CallArgs.add_target_func(name)
        return child

    def _showcore(self, args, kwargs, caller, formatter, opts):
        """
        Do core work of showing the args.
        """
        self.opts = opts
        argtuples = self.get_arg_tuples(caller, args)

        # Construct the result string
        valstr = opts.sep.join([ formatter(name, value, caller, opts) for name, value in argtuples ])
        # print "_showcore valstr:", repr(valstr)
        locval = [ self.call_location(caller) + ":  ", valstr ] if opts.where else [ valstr ]

        # Emit the result string, and optionally return it
        silent = not lambda_eval(opts.show)
        # kwargs['silent'] = silent
        kwargs['retvalue'] = opts.retvalue
        retval = self.fmt(*locval, **kwargs)
        if not silent:
            retval = retval.replace("{", "{{").replace("}", "}}")
            self.say(retval)
        # silence functionality needs hard look
        if opts.retvalue and not silent:
            return retval

    def __gt__(self, other):
        """
        Simple, non-functional call. Experimental.
        """
        opts = self.options.push({})
        caller = inspect.currentframe().f_back

        return self._showcore([other], {}, caller, self.arg_format, opts)

    def __rshift__(self, other):
        """
        Simple, non-functional call. Experimental.
        """
        opts = self.options.push({})
        caller = inspect.currentframe().f_back

        self._showcore([other], {}, caller, self.arg_format, opts)
        return other

        # This doesn't quite work as intended because code parser isn't
        # smart if (show>>a) + (show>>a) appears twice on the same line.

    def __call__(self, *args, **kwargs):
        """
        Main entry point for Show objects.
        """
        opts = self.opts = self.options.push(kwargs)
        caller = inspect.currentframe().f_back
        formatter = self.arg_format_props if opts.props else self.arg_format
        result = self._showcore(args, kwargs, caller, formatter, opts)
        return result

        # FF is (for now) aborted attempt to dive deeper in cases when
        # about to present a highly generic representation. Will need to
        # restructure/refactor _showcore in order to make this work.

        # if result.startswith('<') and result.endswith('>') and ' object at 0x' in result:
            # about to return a generic <__main__.User object at 0x10c73dbd0>
            # so try harder
            # formatter = self.arg_format_props
            # return self._showcore(args, kwargs, caller, formatter, opts)
        # else:
        #    return result

    # TODO: Define __div__ and __truediv__ (for py3) like __call__, but must fix call
    #       position parsing to make that work (ie, different look => different parsing
    #       required)

    def items(self, *args, **kwargs):
        """
        Show items of a collection.
        """
        opts = self.options.push(kwargs)
        caller = inspect.currentframe().f_back
        return self._showcore(args, kwargs, caller, self.arg_format_items, opts)

    def dir(self, *args, **kwargs):
        """
        Show the attributes possible for the given object(s)
        """
        opts = self.options.push(kwargs)
        opts.setdefault('omit', '__*')

        caller = inspect.currentframe().f_back
        return self._showcore(args, kwargs, caller, self.arg_format_dir, opts)

    def pprint(self, *args, **kwargs):
        """
        Show the objects as displayed by pprint. Not well
        integrated as yet. Just a start.
        """
        opts = self.options.push(kwargs)

        caller = inspect.currentframe().f_back
        return self.say(pprint.pformat(*args, **kwargs))

    def props(self, *args, **kwargs):
        """
        Show properties of objects.
        """
        opts = self.opts = self.options.push(kwargs)
        opts.setdefault('omit', '__*')
        if len(args) > 1 and isinstance(args[-1], str):
            used = opts.addflat([args[-1]], ['props'])
            args = args[:-1]
        if opts.sep == Show.options.sep:
            opts.sep = '\n\n'
        caller = inspect.currentframe().f_back
        return self._showcore(args, kwargs, caller, self.arg_format_props, opts)

        # should this check for and show (perhaps with ^ annotation), properties
        # of object inherited from class?

        # if no props, should show normally?
        # Ie less difference between show, show.items, show.props
        # also, maybe more automatic or easy-to-specify truncation of results?

    def locals(self, *args, **kwargs):
        """
        Show all local vars, plus any other values mentioned.
        """
        opts = self.opts = self.options.push(kwargs)
        opts.setdefault('omit', '')
        caller = inspect.currentframe().f_back
        assert not args  # for now
        locdict = caller.f_locals

        to_omit = (opts.omit or '') + ' @py_assert*'
        names = omitnames(locdict.keys(), to_omit)

        # Construct the result string
        valstr = opts.sep.join([ self.arg_format(name, locdict[name], caller, opts) for name in names ])
        locval = [ self.call_location(caller) + ":  ", valstr ] if opts.where else [ valstr ]

        # Emit the result string, and optionally return it
        kwargs['silent'] = not lambda_eval(opts.show)
        kwargs['retvalue'] = opts.retvalue
        print("opts.retvalue:", opts.retvalue)

        retval = self.say(*locval, **kwargs)
        print("retval:", retval)
        if opts.retvalue:
            return retval

    def where(self, *args, **kwargs):
        """
        Show where program execution currently is. Can be used with
        normal output, but generally is intended as a marker.
        """
        opts = self.options.push(kwargs)
        opts.where = True

        caller = inspect.currentframe().f_back
        return self._showcore(args, kwargs, caller, self.arg_format, opts)

    def changed(self, *args, **kwargs):
        """
        Show the local variables, then again only when changed.
        """
        opts = self.opts = self.options.push(kwargs)

        caller = inspect.currentframe().f_back

        f_locals = caller.f_locals
        _id = id(f_locals)

        valitems  = [ (k, v) for (k, v) in f_locals.items() if \
                                not k.startswith('@py_assert') and \
                                not k.startswith('_') and \
                                not isinstance(v, FUNKY) and \
                                not getattr(v, '__module__', '').startswith( ('IPython', 'site', 'show')) and \
                                not (isInteractive and (k == 'In' or k == 'Out'))
                            ]
        if args:
            # self.say("args = {args!r}")
            argtuples = self.get_arg_tuples(caller, args)
            valitems.extend(argtuples)

        valdict = dict(valitems)
        _id = id(f_locals)
        watching = self._watching.get(_id, None)
        if watching is None:
            self._watching[_id] = watching = to_show = valdict
        else:
            to_show = {}
            for k, v in valdict.items():
                if k not in watching or v != watching[k]:
                    to_show[k] = v
                    watching[k] = v

        names = omitnames(to_show.keys(), opts.omit)

        # Construct the result string
        if names:
            valstr = opts.sep.join([ self.arg_format(name, to_show[name], caller, opts) for name in names ])
        else:
            valstr = "no changes" # six.u('\u2205')
        locval = [ self.call_location(caller) + ":  ", valstr ] if opts.where else [ valstr ]

        # Emit the result string, and optionally return it
        kwargs['silent'] = not lambda_eval(opts.show)
        kwargs['retvalue'] = opts.retvalue

        retval = self.say(*locval, **kwargs)
        if opts.retvalue:
            return retval

    def inout(self, *dargs, **dkwargs):
        """
        Show arguments to a function. Decorator itself may
        take arguments, or not. Whavevs.
        """

        # argument prep for decorator with optional arguments
        no_args = False
        if len(dargs) == 1 and not dkwargs and callable(dargs[0]):
            # We were called without args
            func = dargs[0]
            dargs = []
            no_args = True
        mkwargs = self.meth_defaults.get('inout', {}).copy()
        mkwargs.update(dkwargs)
        opts = self.options.push(mkwargs)
        say_kwargs = mkwargs
        only_arg = dkwargs.get("only")
        only_in = only_arg == "in"
        only_out = only_arg == "out"

        def inout_decorator(func):
            """
            Decorator that shows arguments to a function.
            """
            func_code = func.__code__ if _PY3 else func.func_code
            argnames = func_code.co_varnames[:func_code.co_argcount]
            fname = func.__name__ if _PY3 else func.func_name

            def echo_func(*args, **kwargs):
                argitems = list(zip(argnames,args)) + list(kwargs.items())
                argcore = ', '.join('{0}={1!r}'.format(*argtup) for argtup in argitems)
                callstr = ''.join([fname, '(', argcore, ')'])
                fmtcallstr = self.code_repr(callstr)
                if not only_out:
                    self.say(fmtcallstr, **say_kwargs)
                try:
                    retval = func(*args, **kwargs)
                    if not only_in:
                        fmtretval = self.value_repr(retval)
                        retstr = ''.join([fmtcallstr, ' -> ', fmtretval])
                        self.say(retstr, **say_kwargs)
                    return retval
                except Exception as e:  # pragma: no cover
                    raise e

            return echo_func

        if no_args:
            return inout_decorator(func)
        else:
            return inout_decorator

    # TODO: add ability to give methods default styles (like all show.where in red)

    def retval(self, func):
        """
        Decorator that shows arguments to a function, and return value, once
        the function is complete. Similar to inout, but only displays once
        function has returned.
        """
        self.say("WARNING: @show.retval is deprecated", style="red")
        self.say("         Please use @show.inout(only='out') instead", style="red")
        func_code = func.__code__ if _PY3 else func.func_code
        argnames = func_code.co_varnames[:func_code.co_argcount]
        fname = func.__name__ if _PY3 else func.func_name
        opts = self.opts

        def echo_func(*args, **kwargs):
            argitems = list(zip(argnames,args)) + list(kwargs.items())
            argcore = ', '.join('{0}={1!r}'.format(*argtup) for argtup in argitems)
            callstr = ''.join([fname, '(', argcore, ')'])
            fmtcallstr = self.code_repr(callstr)

            say_kwargs = dict(silent=not lambda_eval(opts.show), retvalue=opts.retvalue)

            try:
                retval = func(*args, **kwargs)
                fmtretval = self.value_repr(retval)
                retstr = ''.join([fmtcallstr, ' -> ', fmtretval])

                self.say(retstr, **say_kwargs)
                return retval
            except Exception as e:
                retstr = ''.join([fmtcallstr, ' -> '])

                self.say(retstr, **say_kwargs)
                raise e

        return echo_func

    # TODO: Fold retvalue function into inout, giving inout a control parameter

    def prettyprint(self, mode='ansi', sep='\n', indent=4, width=120, depth=5, style='friendly'):
        """
        Convenience method to turn on pretty-printing. Mode can be text or ansi.
        """
        self.set(sep=sep)
        mode = mode.lower()
        from pprint import pformat
        pf = lambda x: pformat(x, indent=indent, width=width, depth=depth)
        if mode == 'text':
            self.set(fmtfunc=pf)
            return
        elif mode == 'ansi':
            if 'Komodo' in os.environ.get('PYDBGP_PATH', ''):
                self.set(fmtfunc=pf)
                return
            try:
                from pygments import highlight
                from pygments.lexers import PythonLexer
                lexer = PythonLexer()
                from pygments.formatters import Terminal256Formatter
                formatter = Terminal256Formatter(style=style)
                self.set(fmtfunc=lambda x: highlight(pf(x), lexer, formatter).strip())
                self.set(fmtcode=lambda x: highlight(x,     lexer, formatter).strip())
                return
            except ImportError:
                raise ImportWarning('install pygments for ANSI forfmatting; falling back to plain text')
                self.set(fmtfunc=pf)
                return
            except Exception as e:
                raise e
        else:
            raise BadValue("{mode!r} is not a recognized pretty print mode")

    # TODO: Give option for showing return value differently
    # TODO: Give this decorator standard show kwargs
    # TODO: Unify inout and retval function argument/return value decorators

    def method_push(self, base_options, method_name, kwargs):
        """
        Transitional helper function to simplify the grabbing of
        method-specific arguments. Will be phased out as the learnings
        about method arguments are piped back into Options and a more
        long-term API is completed.
        """
        mkwargs = self.meth_defaults.get(method_name, {}).copy()
        mkwargs.update(kwargs)
        if base_options:
            return base_options.push(mkwargs)
        else:
            return mkwargs

    # Promote delegated formatting functions

    def blank_lines(self, *args, **kwargs):
        self.say.blank_lines(*args, **self.method_push(None, 'blank_lines', kwargs))

    def hr(self, *args, **kwargs):
        self.say.hr(*args, **self.method_push(None, 'hr', kwargs))

    def title(self, *args, **kwargs):
        kwargs.setdefault('_callframe', inspect.currentframe().f_back)
        self.say.title(*args, **self.method_push(None, 'title', kwargs))

    def sep(self, *args, **kwargs):
        kwargs.setdefault('_callframe', inspect.currentframe().f_back)
        self.say.sep(*args, **self.method_push(None, 'sep', kwargs))

# Individual settings are needed. For some reason, the group
# setting is just setting the last item. Closure issues?
install_method_setter(Show, 'inout')
install_method_setter(Show, 'blank_lines')
install_method_setter(Show, 'hr')
install_method_setter(Show, 'title')
install_method_setter(Show, 'sep')


show = Show()

# institute nice defaults
show.sep.set(vsep=(1,0))
show.title.set(vsep=1)
# TODO: hoist such defaults into a decorator

# TODO: Should ensure that either instances or classes can have those setters run

class NoShow(Show):
    """
    A Show variant that shows nothing. Maintains just enough context to respond
    as a real Show would. Any clones will also be ``NoShow``s--again, to retain
    similarity. Designed to squelch all output in efficient way, but not
    requiring any changes to the source code. Maintains just enough context to
    """

    options = Show.options.add(
        show   = False,
        retval = False,
    )

    def __init__(self, **kwargs):
        self.options = NoShow.options.push(kwargs)
        self.say = SayReturn(silent=True, retvalue=False)
        self.opts = None  # per call options, set on each call to reflect transient state

    def clone(self, **kwargs):
        """
        Create a child instance whose options are chained to this instance's
        options (and thence to Show.options). kwargs become the child instance's
        overlay options. Because of how the source code is parsed, clones must
        be named via simple assignment.
        """
        return NoShow()

    def _do_nothing(self, *args, **kwargs):
        """
        Fake entry point. Does nothing, returns immediately.
        """
        return None

    __call__ = __gt__ = __rshift__ = _do_nothing
    items = dir = props = locals = changed = inout = retval = _do_nothing
    blank_lines = hr = title = _do_nothing

noshow = NoShow()

# Add show to sys.modules so that "import show" is all you need.
# sys.modules['show'] = show

# Makes some things easier, but seems to have disabled s = Show()
# creation of other show objects. Currently disabled while working on it.

# TODO: add easier decorator for function tracing (just @show?)
