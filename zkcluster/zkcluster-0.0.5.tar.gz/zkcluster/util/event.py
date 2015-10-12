from . import compat


def event_listen(target, event_name, fn):
    getattr(
        target.dispatch,
        event_name
    ).listeners.append(fn)


def _is_event_name(name):
    return not name.startswith('_') and name != 'dispatch'


class _EventMeta(type):
    def __init__(cls, classname, bases, dict_):
        _create_dispatcher(cls, classname, bases, dict_)
        return type.__init__(cls, classname, bases, dict_)


class _Dispatch(object):
    pass


class _DispatchAttr(object):
    __slots__ = 'key',

    def __init__(self, key):
        self.key = key

    def __get__(self, obj, cls):
        ret = _DispatchAttrInst()
        obj.__dict__[self.key] = ret
        return ret


class _DispatchAttrInst(object):
    __slots__ = 'listeners',

    def __init__(self):
        self.listeners = []

    def __call__(self, *arg, **kw):
        for fn in self.listeners:
            fn(*arg, **kw)


def _create_dispatcher(cls, classname, bases, dict_):
    """Create a :class:`._Dispatch` class corresponding to an
    :class:`.Events` class."""

    dispatch_base = _Dispatch

    event_names = [k for k in dict_ if _is_event_name(k)]
    dispatch_cls = type("%sDispatch" % classname,
                        (dispatch_base, ), {})

    dispatch_cls._event_names = event_names

    for k in dispatch_cls._event_names:
        setattr(dispatch_cls, k, _DispatchAttr(k))

    if getattr(cls, '_dispatch_target', None):
        cls._dispatch_target.dispatch = _dispatcher(dispatch_cls)


class _dispatcher(object):
    def __init__(self, event_cls):
        self.event_cls = event_cls

    def __get__(self, obj, cls):
        if obj is None:
            return self.dispatch_cls
        obj.__dict__['dispatch'] = disp = self.event_cls()
        return disp


class EventListener(compat.with_metaclass(_EventMeta, object)):
    """Base class for propagated events.

    Basically is the same as the SQLAlchemy event base; this is a super-minimal
    very basic version of the same thing to avoid SQLAlchemy as a dependency.


    """
    # _dispatch_target = <class>


