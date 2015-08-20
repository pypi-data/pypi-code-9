import sys
import imp

try:
    from importlib import find_loader  # for python3
except ImportError:
    find_loader = None

_import_hooks = {}


def register_import_hook(name, callable_func):
    imp.acquire_lock()

    try:
        hooks = _import_hooks.get(name, None)
        if name not in _import_hooks or hooks is None:
            _import_hooks.get(name)
            module = sys.modules.get(name, None)
            if module is not None:
                _import_hooks[name] = None
                callable_func(module)
            else:
                # No hook has been registered so far so create list and add current hook.
                _import_hooks[name] = [callable_func]
        else:
            # Hook has already been registered, so append current hook.
            _import_hooks[name].append(callable_func)
    finally:
        imp.release_lock()


def _notify_import_hooks(name, module):
    hooks = _import_hooks.get(name, None)

    if hooks is not None:
        _import_hooks[name] = None

        for callable_func in hooks:
            callable_func(module)


class _ImportHookLoader:
    def load_module(self, fullname):
        # Call the import hooks on the module being handled.
        module = sys.modules[fullname]
        _notify_import_hooks(fullname, module)

        return module


class _ImportHookChainedLoader:

    def __init__(self, loader):
        self.loader = loader

    def load_module(self, fullname):
        module = self.loader.load_module(fullname)

        # Call the import hooks on the module being handled.
        _notify_import_hooks(fullname, module)

        return module


class ImportHookFinder:

    def __init__(self):
        self._skip = {}

    def find_module(self, fullname, path=None):
        if fullname not in _import_hooks:
            return None

        # Check whether this is being called on the second time through and return.
        if fullname in self._skip:
            return None
        self._skip[fullname] = True

        try:
            if find_loader:
                loader = find_loader(fullname, path)
                if loader:
                    return _ImportHookChainedLoader(loader)
            else:
                __import__(fullname)

                return _ImportHookLoader()
        finally:
            del self._skip[fullname]


def import_hook(name):
    def decorator(wrapped):
        register_import_hook(name, wrapped)
        return wrapped
    
    return decorator


def import_module(name):
    __import__(name)
    return sys.modules[name]
