"""
setuptools helpers for rust, written by novocaine in rust-python-ext
(https://github.com/novocaine/rust-python-ext), MIT licensed.

Forked at 931232df0e7887f5978eab71e760fb7496d520af for some modifications
and the addition of Distribution.
"""

from __future__ import print_function
import sys
import subprocess
import os.path
import glob
from setuptools import Distribution as BaseDistribution
from distutils.cmd import Command
from distutils.command.install_lib import install_lib
import shutil


class RustBuildCommand(Command):
    """
    Command for building rust crates via cargo.

    Don't use this directly; use the build_rust_cmdclass
    factory method.
    """

    description = 'build rust crates into Python extensions'

    user_options = []

    def _unpack_classargs(self):
        for key, val in self.__class__.args.items():
            setattr(self, key, val)

    def initialize_options(self):
        self._unpack_classargs()

    def finalize_options(self):
        pass

    def run(self):
        try:
            args = ([
                'cargo',
                'build',
                '--manifest-path',
                self.cargo_toml_path,
                '--release',
            ] + list(self.extra_cargo_args or []))
            subprocess.check_output(args)
        except subprocess.CalledProcessError as err:
            raise Exception(
                'cargo failed with code: %d\n%s\n\n'
                'Note you must run rust\'s nightly channel for nahpackpy' %
                (err.returncode, err.output)
            )
        except OSError:
            raise Exception(
                'rust must be installed for extensions to be compiled. '
                'Download the nightly from '
                'https://www.rust-lang.org/install.html'
            )

        target_dir = os.path.join(
            os.path.dirname(self.cargo_toml_path),
            'target/release',
        )

        if sys.platform == 'win32':
            wildcard_so = '*.dll'
        elif sys.platform == 'darwin':
            wildcard_so = '*.dylib'
        else:
            wildcard_so = '*.so'

        try:
            dylib_path = glob.glob(os.path.join(target_dir, wildcard_so))[0]
        except IndexError:
            raise Exception('rust build failed; unable to find any %s in %s' % (
                wildcard_so, target_dir
            ))

        # Ask build_ext where the shared library would go if it had built it,
        # then copy it there.
        build_ext = self.get_finalized_command('build_ext')
        target_fname = os.path.splitext(os.path.basename(dylib_path)[3:])[0]
        ext_path = build_ext.get_ext_fullpath(os.path.basename(target_fname))
        try:
            os.makedirs(os.path.dirname(ext_path))
        except OSError:
            pass
        shutil.copyfile(dylib_path, ext_path)


def build_rust_cmdclass(
        cargo_toml_path,
        debug=False,
        extra_cargo_args=None,
        quiet=False,
    ):
    """
    Args:
        cargo_toml_path (str)   The path to the cargo.toml manifest
                                (--manifest)
        debug (boolean)         Controls whether --debug or --release is
                                passed to cargo.
        extra_carg_args (list)  A list of extra argumenents to be passed to
                                cargo.
        quiet (boolean)         If True, doesn't echo cargo's output.

    Returns:
        A Command subclass suitable for passing to the cmdclass argument
        of distutils.
    """

    # Manufacture a once-off command class here and set the params on it as
    # class members, which it can retrieve later in initialize_options.
    # This is clumsy, but distutils doesn't give you an appropriate
    # hook for passing params to custom command classes (and it does the
    # instantiation).

    _args = locals()

    class RustBuildCommand_Impl(RustBuildCommand):
        args = _args

    return RustBuildCommand_Impl


class install_lib_including_rust(install_lib):
    """
    A replacement install_lib cmdclass that remembers to build_rust
    during install_lib.

    Typically you want to use this so that the usual 'setup.py install'
    just works.
    """

    def build(self):
        install_lib.build(self)
        if not self.skip_build:
            self.run_command('build_rust')


class Distribution(BaseDistribution):

    def has_ext_modules(self):
        # force arch-specific wheel names
        return True
