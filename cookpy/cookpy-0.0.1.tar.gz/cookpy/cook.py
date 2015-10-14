# -*- coding: utf-8 -*-

import re
import os
import subprocess
import sys
import itertools

from . import targets, utils, exceptions
from .const import Modes


class Cook:
    """Manages information regarding the current project."""
    def __init__(self):
        # This will contain strings and functions to assemble when done.
        self._entries = []

        # The base directory is used to determine default values for the output
        # directories and to make paths absolute.
        if sys.argv[0]:
            self._cook_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        else:
            self._cook_dir = os.getcwd()

        # Minimum version of cmake any user should be allowed to use.
        self._cmake_minimum_version = '2.8.11'

        # All directory paths are relative to the current cook.py file.
        self.runtime_dir = 'build/'
        self.library_dir = 'build/'
        self.archive_dir = 'build/'
        self.internal_dir = 'build/.internal/'
        self.cmake_dir = 'build/.internal/'

        # Basic setup: Version requirement, then output directories.
        self.enter(self._compile_cmake_version,
                   self._compile_output_directories)

        # Compute library directories.
        # 1) Every path in the environment variable LIB.
        lib_env = os.environ.get('LIB')
        self._lib_dirs = set()
        if lib_env:
            for directory in lib_env.split(':'):
                if os.path.isdir(directory):
                    self._lib_dirs.add(directory)

        # 2) For every path in the environment variable PATH:
        path_env = os.environ.get('PATH')
        self._path_lib_dirs = set()
        self._path_dirs = set()
        if path_env:
            regex = re.compile(r'(.*)/s?bin')
            for entry in path_env.split(':'):
                # 2.2) The ENTRY itself.
                if os.path.isdir(entry):
                    self._path_dirs.add(entry)

                match = regex.match(entry)
                if match:
                    # 2.1) If ENTRY ends with [s]bin: PREFIX/lib with PREFIX
                    #      being everything before [s]bin, and
                    directory = os.path.join(match.group(1), 'lib')
                    if os.path.isdir(directory):
                        self._path_lib_dirs.add(directory)
                    # 2.2) PREFIX/lib/ARCH with arch being the architecture.
                    # TODO: Arch detection.
                    arch_dir = os.path.join(directory, 'x86_64-linux-gnu')
                    if os.path.isdir(arch_dir):
                        self._path_lib_dirs.add(arch_dir)
                else:
                    # 2.2) Else: ENTRY/lib
                    directory = os.path.join(entry, 'lib')
                    if os.path.isdir(directory):
                        self._path_lib_dirs.add(directory)

    def enter(self, *entries):
        """Append every given element to the list of entries.

        The 'entries' parameter may only contain string or functions
        which return strings.

        @type entries: tuple[str | Function]
        """
        self._entries.extend(entries)

    def abspath(self, p):
        """Return the absolute version of a path.

        The difference between this method and 'os.path.abspath' is
        that the directory of the cook.py file will be used to to make
        the path absolute instead of current working directory.

        @type p: str
        """
        if os.path.isabs(p):
            return p
        else:
            # Calling abspath resolves paths like '/A/./B/..' to '/A'.
            return os.path.abspath(os.path.join(self._cook_dir, p))

    def add_executable(self, name):
        """Create a new executable assigned to this context.

        @type name: str
        @rtype: targets.Executable
        """
        return targets.Executable(self, name)

    def add_library(self, name, mode=Modes.SHARED):
        """Create a new library assigned to this context.

        @type name: str
        @type shared: bool
        @rtype: targets.InternalLibrary
        """
        return targets.InternalLibrary(self, name, mode)

    def import_library(self, path_or_name, mode=Modes.PREFER_SHARED):
        """Import an external library assigned to this context.

        @rtype: targets.ExternalLibrary
        """
        path = self.abspath(path_or_name)

        if not os.path.isfile(path):
            path = self.find_library(path_or_name, mode)
            if path is None:
                raise ValueError

        return targets.ExternalLibrary(self, path, mode)

    def done(self):
        """Write cmake configuration and build project."""
        # Ensure that the paths are absolute.
        cmake_dir = self.abspath(self.cmake_dir)
        internal_dir = self.abspath(self.internal_dir)

        # Make sure the directories which will be used are available.
        utils.make_tree(os.path.dirname(cmake_dir))
        utils.make_tree(internal_dir)

        # Compile the content of the file or catch exceptions.
        try:
            result = '\n'.join(filter(None, (e() if callable(e) else e
                                             for e in self._entries))) + '\n'
        except exceptions.NoSourcesError as exc:
            sys.exit('ERROR: No source files added for target "{}".'
                     .format(exc.target.name))

        # Write every entry to the cmake file.
        with open(os.path.join(cmake_dir, 'CMakeLists.txt'), 'w') as f:
            f.write(result)

        # Start build process. TODO: Install, clean, VS, etc...
        try:
            # Suppress non-error output.
            with open(os.devnull) as null:
                # Pointing CMake to the directory containing the CMakeLists.txt
                # instead of CMakeLists.txt itself leads to building
                # in the current working directory (cwd).
                subprocess.check_call(['cmake', cmake_dir], stdout=null,
                                      cwd=internal_dir)
        except subprocess.CalledProcessError:
            sys.exit(1)

        # Try to install.
        make = subprocess.Popen(['make', 'install'], stderr=subprocess.PIPE,
                                cwd=internal_dir)
        if (make.stderr.readline() == b'make: *** No rule to make target '
                                      b'`install\'.  Stop.\n'):
            make.wait()
            try:
                subprocess.check_call(['make'], cwd=internal_dir)
            except subprocess.CalledProcessError:
                sys.exit(1)
        else:
            while True:
                line = make.stderr.readline().decode()
                if line:
                    print(line)
                else:
                    break

    def find_library(self, name, mode=Modes.PREFER_SHARED, custom=(),
                     standard=True, ignore_case=True):
        """..."""
        generator = custom if not standard else itertools.chain(
            custom, sorted(self._lib_dirs), sorted(self._path_lib_dirs),
            sorted(self._path_dirs))

        # TODO: Remove.
        if mode is Modes.PREFER_STATIC:
            mode = Modes.STATIC
        elif mode is Modes.PREFER_SHARED:
            mode = Modes.SHARED

        # TODO: Implement preference / More formats.
        regex = re.compile(r'(lib)?{}{}$'.format(
            name, '(.a)' if mode is Modes.STATIC else
            '(.so)' if mode is Modes.SHARED else '((.so)|(.a))'),
            re.I if ignore_case else 0)

        for directory in generator:
            for entry in os.listdir(directory):
                if regex.match(entry):
                    return os.path.join(directory, entry)

    def configure(self, path, mapping=None, out=None, **kwargs):
        """..."""
        # TODO: #cmakedefine
        if out is None:
            index = path.rfind('.in')
            if index == -1:
                raise ValueError
            else:
                out = path[:index]

        with open(self.abspath(path), 'r') as source:
            contents = source.read()

        if mapping:
            for key, value in mapping.items():
                contents = contents.replace('@{}@'.format(key), str(value))
        if kwargs:
            for key, value in kwargs.items():
                contents = contents.replace('@{}@'.format(key), str(value))

        if os.path.isfile(out):
            with open(self.abspath(out), 'r') as destination:
                old = destination.read()
            if old != contents:
                with open(self.abspath(out), 'w') as destination:
                    destination.write(contents)
        else:
            with open(self.abspath(out), 'w') as destination:
                    destination.write(contents)

    def glob(self, pathname):
        return utils.glob(self.abspath(pathname))

    def _compile_output_directories(self):
        return '\n'.join([
            'set(CMAKE_LIBRARY_OUTPUT_DIRECTORY {})',
            'set(CMAKE_RUNTIME_OUTPUT_DIRECTORY {})',
            'set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY {})']).format(
            self.abspath(self.library_dir),
            self.abspath(self.runtime_dir),
            self.abspath(self.archive_dir))

    def _compile_cmake_version(self):
        return 'cmake_minimum_required(VERSION {})'.format(
            self._cmake_minimum_version)
