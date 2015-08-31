#! /usr/bin/env python
##########################################################################
# Bredala - Copyright (C) AGrigis, 2015
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
from __future__ import print_function
import sys
import inspect
import time
import numpy
import pprofile


def bredala_signature(obj, is_method=False, use_profiler=True):
    """ Create a decorator that display a function or a class method signature
    and execution time.

    Parameters
    ----------
    obj: callable (mandatory)
        a function or a class method object.
    is_method: bool (optional, default False)
        True if the input object it a method of a class, False otherwise.
    use_profiler: bool (optional, default True)
        if True display the input object execution profile.

    Retruns
    -------
    wrapper: callable
        the decorated input object.
    """
    def wrapper(*args, **kwargs):
        """ Define the input object decorator.
        """
        # Get the function parameters
        arg_spec = inspect.getargspec(obj)
        defaults = [repr(item) for item in arg_spec.defaults or []]
        optional = dict(zip(reversed(arg_spec.args or []), reversed(defaults)))
        for name, value in kwargs.items():
            if name in optional:
                optional[name] = repr(value)
        mandatory = []
        self_parameter = None
        for index in range(len(arg_spec.args) - len(optional)):
            try:
                if index < len(args):
                    value = args[index]
                else:
                    value = kwargs[arg_spec.args[index]]
                if arg_spec.args[index] == "self":
                    self_parameter = value
                if arg_spec.args[index] == "cls":
                    args = args[1:]
                if isinstance(value, list):
                    value_repr = array_repr(numpy.asarray(value))[6:]
                    endindex = value_repr.find("dtype") - 2
                    value_repr = value_repr[:endindex]
                elif isinstance(value, numpy.ndarray):
                    value_repr = array_repr(numpy.asarray(value))
                else:
                    value_repr = repr(value)
                mandatory.append((arg_spec.args[index], value_repr))
            except:
                mandatory.append((arg_spec.args[index], None))
                raise

        # Create the function signature
        params = ["{0}={1}".format(name, val) for name, val in mandatory]
        params.extend([
            "{0}={1}".format(name, val) for name, val in optional.items()])
        signature = "{0}({1})".format(obj.__name__, ", ".join(params))

        # Display a start call message
        module = obj.__module__
        package_name = module.split(".")[0]
        if is_method:
            obj_name = (module + "." + self_parameter.__class__.__name__ +
                        "." + obj.__name__)
        else:
            obj_name = module + "." + obj.__name__
        print("{0}\n[{1}] Calling {2}...\n{3}".format(
            80 * "_", package_name, obj_name, signature))

        # Call
        start_time = time.time()
        if use_profiler:
            profiler = pprofile.Profile()
            returncode = profiler.runcall(obj, *args, **kwargs)
        else:
            returncode = obj(*args, **kwargs)
        duration = time.time() - start_time

        # Display execution profile
        if use_profiler:
            obj_code = inspect.getsourcelines(obj)[0]
            annotate(profiler, sys.stdout, inspect.getmodule(obj).__file__,
                     obj_code)

        # Display an end message
        msg = "{0:.1f}s, {1:.1f}min".format(duration, duration / 60.)
        print(max(0, (80 - len(msg))) * '_' + msg)

        return returncode

    return wrapper


def array_repr(array):
    """ Representation of a numpy array.

    Parameters
    ----------
    array: array (mandatory)
        a numpy array.

    Returns
    -------
    repr: str
        the representation of the numpy array.
    """
    return " ".join([item.strip() for item in repr(array).split("\n")])


def annotate(profiler, out, module_name, obj_code):
    """ Dump annotated input object source code with current profiling
    statistics to 'out' stream. Time unit is second.

    Parameters
    ----------
    profiler: pprofile.Profile (mandatory)
        a profiler.
    out: stream (mandatory)
        destination of annotated input object source code.
    module_name:
        the name of the module of interest (used to filter the execution list).
    obj_code: list of str (mandatory)
        the source code of the object of interest (used to filter the
        execution list).
    """
    # Get the full execution list that will be filtered
    file_dict = profiler.file_dict
    total_time = profiler.total_time
    if not total_time:
        return

    # Define a function to compute pecentage
    def percent(value, scale):
        if scale == 0:
            return 0
        return value * 100 / float(scale)

    # Get all the file profiled
    for name in profiler._getFileNameList(None):

        # Select the module of interest and deal with '.py' '.pyc' extensions
        if module_name.startswith(name):

            # Get line by line execution information
            file_timing = file_dict[name]
            call_list_by_line = file_timing.getCallListByLine()

            # Display the result table header
            print(pprofile._ANNOTATE_HEADER, file=out)
            print(pprofile._ANNOTATE_HORIZONTAL_LINE, file=out)

            # Populate the table with the execution result
            in_obj = False
            for line_item in profiler._iterFile(name, call_list_by_line):

                # Select the portion related to the called object
                lineno, _, _, hits, duration, line = line_item
                if line == obj_code[0]:
                    in_obj = True

                # Display the execution status
                if in_obj:
                    if hits:
                        time_per_hit = duration / hits
                    else:
                        time_per_hit = 0
                    print(pprofile._ANNOTATE_FORMAT % {
                        "lineno": lineno,
                        "hits": hits,
                        "time": duration,
                        "time_per_hit": time_per_hit,
                        "percent": percent(duration, total_time),
                        "line": line,
                    }, end="", file=out),

                # Select the portion related to the called object
                if line == obj_code[-1]:
                    in_obj = False
