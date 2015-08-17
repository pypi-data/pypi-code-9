# Copyright Louis Paternault 2015
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""Plugin loader"""

import collections
import contextlib
import functools
import logging
import os
import shlex
import sys

from evariste import errors, utils, setup
from evariste.hooks import methodhooks
import evariste

LOGGER = logging.getLogger(evariste.__name__)

class NoMatch(errors.EvaristeError):
    """No plugin found matching ``value``."""

    def __init__(self, value, available):
        super().__init__()
        self.value = value
        self.available = available

    def __str__(self):
        return "Value '{}' does not match any of {}.".format(
            self.value,
            str(self.available),
            )

class SameKeyword(errors.EvaristeError):
    """Two plugins have the same keyword."""

    def __init__(self, keyword, plugin1, plugin2):
        super().__init__()
        self.keyword = keyword
        self.plugins = (plugin1, plugin2)

    def __str__(self):
        return """Plugins '{}' and '{}' have the same keyword '{}'.""".format(
            self.plugins[0].__name__,
            self.plugins[1].__name__,
            self.keyword,
            )

class NotAPlugin(errors.EvaristeError):
    """Superclass of plugins is not a plugin."""

    def __init__(self, obj):
        super().__init__()
        self.obj = obj

    def __str__(self):
        return (
            """Class '{obj.__module__}.{obj.__name__}' is not a plugin """
            """(it should inherit from """
            """'{superclass.__module__}.{superclass.__name__}')."""
            ).format(
                obj=self.obj,
                superclass=PluginBase,
            )

class PluginNotFound(errors.EvaristeError):
    """Plugin cannot be found."""

    def __init__(self, plugin_type, keyword):
        super().__init__()
        self.plugin_type = plugin_type
        self.keyword = keyword

    def __str__(self):
        return "Cannot found plugin '{}.{}'.".format(
            self.plugin_type,
            self.keyword,
            )

@functools.total_ordering
class PluginBase:
    """Plugin base: all imported plugins must be subclasses of this class."""
    keyword = None
    description = None
    priority = 0
    default_setup = {}
    global_default_setup = {}
    plugin_type = None
    subplugins = {}
    hooks = {}
    depends = {}
    default = False
    required = False

    def __init__(self, shared):
        self.hook_instances = {}
        self.shared = shared
        self.local = shared.get_plugin_view(self.plugin_id)
        self._set_default_setup()
        self._load_hooks()

    def _set_default_setup(self):
        """Set default value for this plugin setup, if necessary."""
        default = setup.Setup()
        for parent in reversed(self.__class__.mro()): # pylint: disable=no-member
            if hasattr(parent, "default_setup"):
                default.update(parent.global_default_setup)
                default.update({self.plugin_id: parent.default_setup})
        self.shared.setup.fill_blanks(default)

    def _load_hooks(self):
        """Load hooks."""
        for hook in self.hooks:
            self.hook_instances[hook] = functools.partial(self.hooks[hook], self)

    def match(self, value, *args, **kwargs): # pylint: disable=unused-argument
        """Return ``True`` iff ``value`` matches ``self``.

        Default is keyword match. This method can be overloaded by
        subclasses.
        """
        return value == self.keyword

    @property
    def plugin_id(self):
        """Return the name of the section of the object, in the setup file."""
        return "{}.{}".format(self.plugin_type, self.keyword)

    def __lt__(self, other):
        priority = self.priority
        if callable(priority):
            priority = priority() # pylint: disable=not-callable
        other_priority = other.priority
        if callable(other_priority):
            other_priority = other_priority()
        if priority == other_priority:
            return self.keyword < other.keyword
        return priority < other_priority

class PluginLoader:
    """Plugin loader. Find plugins and select the appropriate one."""

    def __init__(self, shared, libdirs=None):
        self.plugins = self._load_plugins(
            self._sort_plugins(
                self._list_available_plugins(libdirs)
                ),
            shared,
            )

    @staticmethod
    def _sort_plugins(pluginset):
        """Sort plugins by type and keyword."""
        plugindict = collections.defaultdict(dict)

        for plugin in pluginset:
            if plugin.plugin_type not in ["readme", "target"]:
                if plugin.keyword in plugindict[plugin.plugin_type]:
                    raise SameKeyword(
                        plugin.keyword,
                        plugin,
                        plugindict[plugin.plugin_type][plugin.keyword],
                        )

                plugindict[plugin.plugin_type][plugin.keyword] = plugin
            for subtype in plugin.subplugins:
                key = "{}.{}.{}".format(plugin.plugin_type, plugin.keyword, subtype)
                for candidate in pluginset:
                    if (
                            candidate.plugin_type == subtype
                            and
                            issubclass(candidate, plugin.subplugins[subtype])
                        ):
                        plugindict[key][candidate.keyword] = candidate

        return plugindict

    @staticmethod
    def _load_plugins(available, shared):
        """Given the avaialble plugins, only loads relevant plugins.

        :return: A dictionary of loaded (instanciated) plugins.
        """
        # pylint: disable=too-many-branches

        # Step 0: Converting setup options in a list of keyword
        for plugin_type in available:
            for key in ["enable_plugins", "disable_plugins"]:
                if shared.setup[plugin_type][key] is None:
                    shared.setup[plugin_type][key] = []
                else:
                    if isinstance(shared.setup[plugin_type][key], str):
                        shared.setup[plugin_type][key] = shlex.split(shared.setup[plugin_type][key])
                    elif isinstance(shared.setup[plugin_type][key], list):
                        pass
                    else:
                        raise ValueError(
                            (
                                "'Setup[{}][enable_plugins]' should be a string or a "
                                "list (is now {}: '{}')."
                            ).format(
                                plugin_type,
                                type(shared.setup[plugin_type][key]),
                                shared.setup[plugin_type][key],
                                ))

        # Step 1: Adding default plugins (unless disabled), and required plugins
        plugins = collections.defaultdict(dict)
        for plugin_type in available:
            for keyword in available[plugin_type]:
                if (
                        available[plugin_type][keyword].default
                        and
                        keyword not in shared.setup[plugin_type]['disable_plugins']
                    ):
                    plugins[plugin_type][keyword] = available[plugin_type][keyword]
                if available[plugin_type][keyword].required:
                    if keyword in shared.setup[plugin_type]["disable_plugins"]:
                        LOGGER.warning(
                            (
                                "Disabling plugin '{}.{}' is asked by setup, "
                                "but it is required. Still enabling."
                            ).format(
                                plugin_type,
                                keyword,
                                )
                            )
                    plugins[plugin_type][keyword] = available[plugin_type][keyword]

        # Step 2: Adding enabled plugins
        for plugin_type in available:
            for keyword in shared.setup[plugin_type]["enable_plugins"]:
                try:
                    plugins[plugin_type][keyword] = available[plugin_type][keyword]
                except KeyError:
                    raise PluginNotFound(plugin_type, keyword)

        # Step 3: Managing dependencies
        to_process = []
        for plugin_type in plugins:
            to_process.extend(plugins[plugin_type].values())
        while to_process:
            plugin = to_process.pop()
            if 'required' in plugin.depends:
                for plugin_type in plugin.depends['required']:
                    for keyword in plugin.depends['required'][plugin_type]:
                        try:
                            required = available[plugin_type][keyword]
                        except KeyError:
                            raise PluginNotFound(plugin_type, keyword)
                        if keyword not in plugins[plugin_type]:
                            if keyword in shared.setup[plugin_type]["disable_plugins"]: # pylint: disable=line-too-long
                                LOGGER.warning(
                                    (
                                        "Disabling plugin '{}.{}' is asked by "
                                        "setup, but it is required. Still "
                                        "enabling."
                                    ).format(
                                        plugin_type,
                                        keyword,
                                        )
                                )
                            plugins[plugin_type][keyword] = required
                            to_process.append(required)
            if 'suggested' in plugin.depends:
                for plugin_type in plugin.depends['suggested']:
                    for keyword in plugin.depends['suggested'][plugin_type]:
                        try:
                            suggested = available[plugin_type][keyword]
                        except KeyError:
                            LOGGER.warning(
                                (
                                    "Ignoring plugin '{}.{}' required by "
                                    "'{}.{}': plugin not found."
                                ).format(
                                    plugin_type, keyword, plugin.plugin_type, plugin.keyword
                                ))
                            continue
                        if suggested.keyword not in plugins[plugin_type]:
                            if suggested.keyword in shared.setup[plugin_type]["disable_plugins"]:
                                continue
                            plugins[plugin_type][suggested.keyword] = suggested
                            to_process.append(suggested)

        # Step 4: Instanciating plugins
        loaded = collections.defaultdict(dict)
        for plugin_type in plugins:
            for keyword in plugins[plugin_type]:
                loaded[plugin_type][keyword] = plugins[plugin_type][keyword](shared)

        return loaded

    @staticmethod
    def _list_available_plugins(libdirs):
        """Look for available plugins in accessible packages.

        Return a set of available plugins.
        """
        plugins = set()
        if libdirs is None:
            libdirs = []

        path = []
        path.extend([
            os.path.join(utils.expand_path(item), "plugins")
            for item
            in [".evariste", "~/.config/evariste", "~/.evariste"]
            ])
        path.extend([utils.expand_path(item) for item in libdirs])
        path.extend([
            os.path.join(item, "evariste")
            for item
            in sys.path
            ])

        for module in utils.iter_modules(path, "evariste.", LOGGER.debug):
            for attr in dir(module):
                if attr.startswith("_"):
                    continue
                obj = getattr(module, attr)

                if (
                        isinstance(obj, type)
                        and
                        issubclass(obj, PluginBase)
                    ):
                    if obj.keyword is None:
                        continue
                    plugins.add(obj)
        return plugins

    def match(self, plugin_type, value):
        """Return the first plugin matching ``value``.

        A plugin ``Foo`` matches ``value`` if ``Foo.match(value)`` returns
        True.
        """
        for plugin in sorted(self.get_plugin_type(plugin_type).values(), reverse=True):
            if plugin.match(value):
                return plugin
        raise NoMatch(value, sorted(self.iter_keywords(plugin_type)))

    def iter_pluginid(self, plugin_type=None):
        """Iterate over plugin ids."""
        for plugin in self.iter_plugins(plugin_type):
            yield plugin.plugin_id

    def iter_plugins(self, plugin_type=None):
        """Iterate over plugins."""
        if plugin_type is None:
            for plugin_type in self.plugins:
                for keyword in self.get_plugin_type(plugin_type):
                    yield self.get_plugin_type(plugin_type)[keyword]
        else:
            for keyword in self.get_plugin_type(plugin_type):
                yield self.get_plugin_type(plugin_type)[keyword]

    def iter_keywords(self, plugin_type=None):
        """Iterate over keywords"""
        if plugin_type is None:
            for plugin_type in self.plugins:
                yield from self.get_plugin_type(plugin_type)
        else:
            yield from self.get_plugin_type(plugin_type)

    def get_plugin_type(self, plugin_type):
        """Return a dictionary of plugins of the given type.

        This dictionary is indexed by plugin keywords.
        """
        return self.plugins[plugin_type]

    def get_plugin(self, plugin_id):
        """Return the plugin with the given id."""
        for plugin in self.iter_plugins():
            if plugin.plugin_id == plugin_id:
                return plugin
        raise KeyError(plugin_id)


def get_plugins(self, *_args, **_kwargs):
    """Given a :class:`AllPlugins` object, return itself.

    Useful to give hooks the plugins object.
    """
    return self

def get_libdirs(libdirs):
    """Convert `libdirs` setup option (as a string) to a list of path (as strings).
    """
    if libdirs:
        return shlex.split(libdirs)
    else:
        return []

class AllPlugins:
    """Gather all used plugins."""
    # pylint: disable=too-few-public-methods

    @methodhooks(name="load_plugins", pre=False, getter=get_plugins)
    def __init__(self, *, shared):
        self.shared = shared
        self.plugins = PluginLoader(
            shared,
            get_libdirs(shared.setup['setup']['libdirs']),
            )

    def iter_plugins(self, *args, **kwargs):
        """Iterate over loaded plugins."""
        yield from self.plugins.iter_plugins(*args, **kwargs)

    def _iter_hooks(self, name):
        """Iterator over functions registered for hook ``name``."""
        for plugin in self.iter_plugins():
            if name in plugin.hook_instances:
                yield plugin.hook_instances[name](self.shared)

    def apply_hook(self, name, function, *, pre=True, post=True, args=None, kwargs=None):
        """Apply hook ``name``.

        :param str name: Name of the hook to apply.
        :param function function: Function to which the hook is to be applied.
        :param bool pre: Enable pre-hook.
        :param bool post: Enable post-hook.
        :param list args: List of parameters to pass to hooks and
            ``function``.
        :param dict kwargs: Dictionary of parameters to pass to hooks and
            ``function``.
        """
        if args is None:
            args = list()
        if kwargs is None:
            kwargs = dict()
        hooks = None
        if pre:
            hooks = list(self._iter_hooks(name))
            for hook in hooks:
                returnvalue = hook.pre(*args, **kwargs)
                if returnvalue is not None:
                    args, kwargs = returnvalue
        returnvalue = function(*args, **kwargs)
        if post:
            if hooks is None:
                hooks = list(self._iter_hooks(name))
            for hook in hooks:
                returnvalue = hook.post(returnvalue)
        return returnvalue

    @contextlib.contextmanager
    def contexthook(self, name, *, args=None, kwargs=None):
        """Context, adding hooks at the beginning and end of ``with`` statement.

        :param str name: Name of the hook.
        :param list args: List of arguments to pass to the hooks.
        :param dict kwargs: Dictonary of arguments to pass to the hooks.
        """
        if args is None:
            args = list()
        if kwargs is None:
            kwargs = dict()
        hooks = list(self._iter_hooks(name))
        for hook in hooks:
            hook.pre(*args, **kwargs)
        yield
        for hook in hooks:
            hook.post()

    def get_plugin(self, plugin_id):
        """Return the plugin with the given id."""
        return self.plugins.get_plugin(plugin_id)

    def get_plugin_type(self, plugin_type):
        """Return a dictionary of plugins of the given type."""
        return self.plugins.get_plugin_type(plugin_type)

    def match_plugin(self, *args, **kwargs):
        """Return the first plugin matching the arguments.

        Arguments are transmitted to
        :meth:`evariste.plugins.PluginLoader.match`.
        """
        return self.plugins.match(*args, **kwargs)

    def iter_pluginid(self):
        """Iterate over plugin id."""
        yield from self.plugins.iter_pluginid()
