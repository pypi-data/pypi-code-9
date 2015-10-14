# -*- coding: utf-8 -*-

import random
import string
import itertools
import collections

from . import utils, exceptions
from .const import Modes


class Target:
    """Base class for all targets."""
    def __init__(self, cook, name):
        """
        @type cook: cookpy.Cook
        @type name: str
        """
        self._cook = cook
        self.name = name
        self._install = False

        self._cook.enter(self._compile_init,
                         self._compile_install)

    def install(self):
        self._install = True

    def _compile_init(self):
        """Internal function which compiles the initialization."""
        raise NotImplementedError

    def _compile_install(self):
        if self._install:
            return 'install(TARGETS {} DESTINATION {})'.format(
                self.name, self._cook.abspath('./'))


class InternalTarget(Target):
    """Base class for all targets build by the project.

    Internal targets differ from targets in that they are compiled by
    this project. This obviously means that it is possible to add source
    files, link libraries to this target, include header files, etc.
    """
    def __init__(self, cook, name):
        """
        @type cook: cookpy.Cook
        @type name: str
        """
        Target.__init__(self, cook, name)

        self.sources = set()
        self.language = None
        self.links = []
        self.includes = set()
        self.flags = collections.OrderedDict()

        self._cook.enter(self._compile_includes,
                         self._compile_links,
                         self._compile_language,
                         self._compile_flags)

    def add(self, *sources, glob=True):
        """Append every given source to the source list.

        Each argument must be either a string or a string-yielding iterable.

        @type sources: tuple[str | Iterable]
        @rtype: InternalTarget
        """
        for iterable in sources:
            if isinstance(iterable, str):
                iterable = [iterable]
            for source in iterable:
                if not isinstance(source, str):
                    raise TypeError('cannot add {} - must be of type str'
                                    .format(source))
                if glob:
                    self.sources.update(self._cook.glob(source))
                else:
                    self.sources.add(self._cook.abspath(source))
        return self

    def include(self, *directories, glob=True):
        """Include the given directories to this target.

        Each argument must be either a string or a string-yielding iterable.

        @type directories: tuple[str | Iterable]
        @rtype: InternalTarget
        """
        for iterable in directories:
            if isinstance(iterable, str):
                iterable = [iterable]
            for include in iterable:
                if not isinstance(include, str):
                    raise TypeError('cannot include {} - must be of type str'
                                    .format(include))
                if glob:
                    self.includes.update(self._cook.glob(include))
                else:
                    self.includes.add(self._cook.abspath(include))
        return self

    def exclude(self, *directories, glob=True):
        """Exclude the given directories from this target.

        Each argument must be either a string or a string-yielding iterable.

        @type directories: tuple[str | Iterable]
        @rtype: InternalTarget
        """
        for iterable in directories:
            if isinstance(iterable, str):
                iterable = [iterable]
            for include in iterable:
                if not isinstance(include, str):
                    raise TypeError('cannot include {} - must be of type str'
                                    .format(include))
                if glob:
                    self.includes.difference_update(self._cook.glob(include))
                else:
                    self.includes.discard(self._cook.abspath(include))
        return self

    def remove(self, *sources, glob=True):
        """Remove every given source from the source list.

        Each argument must be either a string or a string-yielding iterable.

        @type sources: tuple[str | Iterable]
        @rtype: InternalTarget
        """
        for iterable in sources:
            if isinstance(iterable, str):
                iterable = [iterable]
            for source in iterable:
                if not isinstance(source, str):
                    raise TypeError('cannot remove {} - must be of type str'
                                    .format(source))
                if glob:
                    self.sources.difference_update(self._cook.glob(source))
                else:
                    self.sources.discard(self._cook.abspath(source))
        return self

    def link(self, *libraries, mode=Modes.PREFER_SHARED):
        """Link every given library to this target.

        Each argument must be either a library or a library-yielding iterable.

        @type libraries: tuple[Library | Iterable]
        @rtype: InternalTarget
        """
        for iterable in libraries:
            if isinstance(iterable, (Library, str)):
                iterable = [iterable]
            for library in iterable:
                if isinstance(library, str):
                    library = self._cook.find_library(library)
                if not isinstance(library, (Library, str)):
                    raise TypeError('cannot link {} - must be of type Library '
                                    'or str'.format(library))
                self.links.append(library)
        return self

    def set_language(self, language):
        """Set the language of this target.

        @param language: str
        @rtype: InternalTarget
        """
        self.language = language
        return self

    def flag(self, name, value=None):
        """
        @param name: str
        @param value: str
        @rtype: InternalTarget
        """
        self.flags[name] = value
        return self

    def _compile_init(self):
        # This is just here for completeness.
        raise NotImplementedError

    def _compile_includes(self):
        """Internal function which compiles the include directories."""
        if self.includes:
            return 'target_include_directories({})'.format(' '.join(
                itertools.chain([self.name, 'PRIVATE'], self.includes)))

    def _compile_links(self):
        """Internal function which compiles the links."""
        if self.links:
            return 'target_link_libraries({})'.format(' '.join(
                itertools.chain([self.name], (l.name if isinstance(l, Library)
                                              else l for l in self.links))))

    def _compile_language(self):
        """Internal function which compiles the language."""
        # TODO: REMOVE?
        if self.language:
            return 'set_target_properties({})'.format(' '.join(
                [self.name, 'PROPERTIES', 'LINKER_LANGUAGE',
                 utils.convert_language_name(self.language)]))

    def _compile_flags(self):
        if self.flags:
            flags = ' '.join(('{}={}'.format(name, value) if value else name
                              for name, value in self.flags.items()))
            return 'set_target_properties({})'.format(' '.join([
                self.name, 'PROPERTIES', 'COMPILE_FLAGS',
                '"{}"'.format(flags)]))

    def _compile_output_directories(self):
        pass


class Library(Target):
    """Common functionality between imported and internal libraries."""
    def link_to(self, *targets):
        """Link this library to every given target.

        Each argument must be either an internal target or an
        internal-target-yielding iterable.

        @type targets: tuple[InternalTarget | Iterable]
        @rtype: Library
        """
        for iterable in targets:
            if isinstance(iterable, InternalTarget):
                iterable = [iterable]
            for target in iterable:
                if not isinstance(target, InternalTarget):
                    raise TypeError('cannot link to {} - must be of type '
                                    'InternalTarget'.format(target))
                target.link(self)
        return self

    def _compile_init(self):
        # This is just here for completeness.
        raise NotImplementedError


class Executable(InternalTarget):
    """Represents an executable."""
    def _compile_init(self):
        if not self.sources:
            raise exceptions.NoSourcesError(self)
        return 'add_executable({})'.format(' '.join(
            itertools.chain([self.name], self.sources)))


class InternalLibrary(InternalTarget, Library):
    """Internal Library."""
    def __init__(self, cook, name, mode):
        InternalTarget.__init__(self, cook, name)
        self.mode = mode

    def _compile_init(self):
        if not self.sources:
            raise exceptions.NoSourcesError(self)

        if self.mode is not Modes.STATIC and self.mode is not Modes.SHARED:
            input(self.mode)
            raise ValueError

        return 'add_library({} {} {})'.format(
            self.name, 'SHARED' if self.mode.value else 'STATIC',
            ' '.join(self.sources))


class ExternalLibrary(Library):
    """Imported library."""
    def __init__(self, cook, path, mode=Modes.ANY):
        Library.__init__(self, cook, self._generate_name())
        self.mode = mode
        self.path = path

    def _compile_init(self):
        if self.mode is Modes.STATIC or self.mode is Modes.SHARED:
            mode = self.mode.value
        else:
            mode = utils.determine_mode(self.path).value

        return '\n'.join([
            'add_library({} {} IMPORTED)'.format(
                self.name, mode),
            'set_target_properties({} PROPERTIES IMPORTED_LOCATION {})'.format(
                self.name, self.path)])

    @staticmethod
    def _generate_name():
        return 'IMPORTED_' + ''.join(random.choice(string.ascii_uppercase)
                                     for _ in range(16))
