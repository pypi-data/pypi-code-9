import functools
import six

from ioc.exc import DependencyDoesNotExist
from ioc.exc import MissingDependency


class Dependency(object):
    """Consumers use the :class:`.Dependency` object to declare a
    dependency.

    Args:
        mode: options for the dependency behavior.
        registry: the registry holding the dependencies.
        names: a list of named dependencies that satisfy the requirement.
            The first satifsying dependency will be used by the wrapping
            :class:`.Dependency` object.
        methods: a list of strings or :class:`.Signature` instances that
            specify the required methods, and optionally their signature.
        args: the default arguments for a function call.
        kwargs: specifies the keyword arguments; will override the caller
            if mode is ``KW_OVERRIDE``, else they are used as defaults
            (the default behavior).
    """

    def __init__(self, registry, mode, names, methods=None, args=None, kwargs=None):
        self.registry = registry
        self.names = [names] if isinstance(names, str) else names
        self.methods = methods or []
        self.using = None
        self.provided = self.registry.NOT_PROVIDED
        self.args = args
        self.kwargs = kwargs

    def is_satisfied(self):
        """Return ``True`` if the dependency is satisied by the provider."""
        return self.provided != self.registry.NOT_PROVIDED

    def setup(self, ignore_missing=False):
        """Setup the dependency.

        Args:
            ignore_missing: ``True`` if meth:`setup()` should not raise an
                exception if the dependency is missing. Default is ``False``.

        Returns:
            None
        """
        # Get the first matching dependency from the
        # registry.
        for name in self.names:
            if name not in self.registry:
                continue
            self.using = name

        if self.using is None:
            if not ignore_missing:
                raise MissingDependency(self, self.names)
            return

        dep = self.registry[self.using]
        if self.args is not None:
            dep = functools.partial(dep, *self.args)

        self.provided = dep

    def teardown(self):
        """Tears down the configured dependency for re-initialization."""
        self.using = None
