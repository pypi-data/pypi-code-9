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

"""Builder

Takes care of build process.
"""

import functools
import logging
import os

from evariste import plugins
from evariste import multithread
from evariste.cache import open_cache
from evariste.hooks import methodhooks
from evariste.plugins import AllPlugins
from evariste.setup import Setup, SetupError
from evariste.tree import Root
import evariste

LOGGER = logging.getLogger(evariste.__name__)

class Builder:
    """Takes care of build process. Can be used as a context.
    """
    # pylint: disable=no-member

    def __init__(self, setup, cachedir=None):
        self.cache = open_cache(cachedir, setup, self)
        self.shared = self.cache.shared
        self.plugins = AllPlugins(shared=self.shared)
        self.lock = multithread.Lock()

        LOGGER.info("Building directory tree…")
        try:
            with self.plugins.contexthook("buildtree", args=[self]):
                self.tree = Root.from_vcs(
                    self.plugins.match_plugin('vcs', self.shared.setup['setup']['vcs']),
                    )
        except plugins.NoMatch as error:
            raise SetupError(
                "Setup error: Value '{}' is not a valid vcs (available ones are: {}).".format(
                    error.value,
                    ", ".join(["'{}'".format(item) for item in error.available]),
                    )
                )

    @methodhooks(name="compiletree")
    def compile(self):
        """Compile files handled by this builder."""
        LOGGER.info("Compiling…")
        self.tree.root_compile()
        self.prune_readmes()

    def prune_readmes(self):
        """Remove readme files from tree."""
        for plugin in self.plugins.get_plugin_type('renderer').values():
            plugin.prune_readmes(self.tree)

    @methodhooks()
    def close(self):
        """Perform close operations."""
        self.cache.close()

    @classmethod
    def from_setupname(cls, name, *, cachedir=None, default=None):
        """Factory that returns a builder, given the name of a setup file."""
        LOGGER.info("Reading setup…")
        setup = Setup.from_file(name).update(default)
        if cachedir is None:
            if setup['setup']['cachedir'] is not None:
                cachedir = setup['setup']['cachedir']
            else:
                cachedir = '.{}.cache'.format(os.path.basename(name))
        if default is None:
            default = {}
        return cls(
            setup,
            os.path.join(
                os.path.dirname(name),
                cachedir,
                ),
            )

    @classmethod
    def from_setupdict(cls, dictionary, *, cachedir=None, default=None):
        """Factory that returns a builder, given a setup dictionary."""
        LOGGER.info("Reading setup…")
        if default is None:
            default = {}
        if cachedir is None:
            try:
                cachedir = dictionary['setup']['cachedir']
            except KeyError:
                pass
        return cls(Setup.from_dict(dictionary).fill_blanks(default), cachedir)

    def renderer(self, keyword):
        """Returns a :func:`functools.partial` object over the `keyword` renderer.
        """
        return functools.partial(self.plugins.match_plugin("renderer", keyword).render, self.tree)

    def iter_renderers(self):
        """Iterator over renderers.

        Returns a :func:`functools.partial` object, over the renderer
        :meth:`render` method, with tree as the first argument. More arguments
        can be added when calling the partial object.
        """
        for keyword in self.shared.setup["renderer"]["enable_plugins"]: # pylint: disable=no-member
            LOGGER.info("Rendering {}…".format(keyword))
            yield self.renderer(keyword)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.close()
        return False
