#! /usr/bin/env python
##########################################################################
# Bredala - Copyright (C) AGrigis, 2015
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
#
# From: http://code.activestate.com/recipes/577742
##########################################################################

# System import
import sys
import inspect
import types

# Bredala import
import bredala


class Decorations(object):
    """ A class that docorate a module functions based on the factory, ie.
    the '_modules' mapping.
    """
    def hack(self, module, name):
        """ Method invoked to transform the input module.

        Parameters
        ----------
        module: object (mandatory)
            a python module object.
        name: str (mandatory)
            the name of the input module.

        Returns
        -------
        decorated_module: object
            if a decorator has been registered for this module in the registery
            return the decorated input python module object, otherwise directly
            the input python module object.
        """
        # If a decorator is decalred for the module apply it now
        for decorator_struct in bredala._modules.get(name, ()):
            self.decorate(module, decorator_struct["decorator"],
                          decorator_struct["names"], name)
        return module

    def decorate(self, module, decorator, names, name):
        """ Method that decorates function and class methods.

        Parameters
        ----------
        module: object (mandatory)
            a python module object.
        decorator: callable (mandatory)
            a decorator function that will be applied on all the input module
            slected functions and methods.
        names: list of str (mandatory)
            a list of function or methods we want to decorate, if None all the
            module functions or methods will be decorated.
        name: str (mandatory)
            the name of the input module.
        """
        # Create a class mapping
        mapping = {}
        if names is not None:
            for filter_name in names:
                kname, mname = Decorations.split_class(filter_name)
                mapping.setdefault(kname, []).append(mname)

        # Walk on all the module items
        for module_attr, module_object in module.__dict__.items():

            # Function case
            if isinstance(module_object, types.FunctionType):
                if names is None or module_object.__name__ in names:
                    setattr(module, module_attr, decorator(module_object,
                            use_profiler=bredala.USE_PROFILER))
            # Class case
            elif inspect.isclass(module_object):
                if names is None or module_object.__name__ in mapping:
                    if names is None:
                        allowed_methods = [None]
                    else:
                        allowed_methods = mapping[module_object.__name__]
                    if sys.version_info[:2] >= (3, 0):
                        methods = inspect.getmembers(
                            module_object, predicate=inspect.isfunction)
                    else:
                        methods = inspect.getmembers(
                            module_object, predicate=inspect.ismethod)
                    for method_name, method in methods:
                        if (None in allowed_methods or
                                method_name in allowed_methods):
                            setattr(module_object, method_name, decorator(
                                    method, True,
                                    use_profiler=bredala.USE_PROFILER))

    @classmethod
    def split_class(cls, name):
        """ Split a  module name.

        Parameters
        ----------
        name: str (mandatory)
            a name describing a class or a class method: <klass> or
            <klass>.<method>.

        Returns
        -------
        kname: str
            the class name.
        mname: str
            the associated module name.
        """
        if "." in name:
            try:
                kname, mname = name.split(".")
            except:
                raise ValueError("'{0}' is not a valid name class or class "
                                 "method description.".format(name))
        else:
            kname = name
            mname = None
        return kname, mname
