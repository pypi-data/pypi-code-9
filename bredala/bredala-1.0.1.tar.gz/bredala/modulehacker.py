#! /usr/bin/env python
##########################################################################
# Bredala - Copyright (C) AGrigis, 2015
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
#
# From: http://code.activestate.com/recipes/577742
# And: https://www.python.org/dev/peps/pep-0302/
##########################################################################

# System import
import sys
import os
import inspect
import imp

# Bredala import
import bredala
from .signaturedecorator import bredala_signature
from.decorations import Decorations


def register(module, decorator=bredala_signature, names=None):
    """ Function to register a decorator for a list of module names.

    Parameters
    ----------
    decorator: callable (mandatory)
        a decorator function.
    module: str (mandatory)
        a module name whose functions will be decorated.
    names: list of str (optional, default None)
        a list of function or methods we want to decorate, if None all the
        module functions or methods will be decorated.
    """
    if module not in bredala._modules:
        bredala._modules[module] = []
    bredala._modules[module].append({"decorator": decorator, "names": names})


def modulehacker_register(obj):
    """ A simple registery to define new hackers.
    """
    bredala._hackers.append(obj)


class BredalaMetaImportHook(object):
    """ A class that import a module like normal and then passed to a hacker
    object that gets to do whatever it wants to the module. Then the return
    value from the hack call is put into sys.modules.
    """
    def __init__(self):
        self.module = None

    def find_module(self, name, path=None):
        """ This method is called by Python if this class is on sys.path.
        'name' is the fully-qualified name of the module to look for, and
        'path' is either __path__ (for submodules and subpackages) or None (for
        a top-level module/package).

        Note that this method will be called every time an import statement
        is detected (or __import__ is called), before Python's built-in
        package/module-finding code kicks in.
        """
        # Use this loader only on registered modules
        if name not in bredala._modules:
            return None

        self.sub_name = name.split(".")[-1]
        self.mod_name = name.rpartition(".")[0]
        try:
            self.file, self.filename, self.stuff = imp.find_module(
                self.sub_name, path)
            self.path = [self.filename]
        except ImportError:
            return None

        return self

    def load_module(self, name):
        """ This method is called by Python if BredalaImportHook 'find_module'
         does not return None. 'name' is the fully-qualified name
         of the module/package that was requested.
        """
        module = imp.load_module(name, self.file, self.filename,
                                 self.stuff)
        if self.file:
            self.file.close()
        for hacker in bredala._hackers:
            module = hacker.hack(module, name)
        module.__path__ = self.path
        module.__loader__ = self
        module.__package__ = name
        module.__name__ = name
        if self.stuff[0] == ".py":
            module.__file__ = self.path[0]
        else:
            module.__file__ = os.path.join(self.path[0], "__init__.py")

        return module


modulehacker_register(Decorations())
sys.meta_path.insert(0, BredalaMetaImportHook())
