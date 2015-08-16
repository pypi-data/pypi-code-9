# Copyright (C) 2011-2014 Jens Kasten. All Rights Reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
# 

"""
FF package for RSBAC FF module.

Copyright (C) Jens Kasten. All Rights Reserved.
"""

__author__  = "Jens Kasten <jens@kasten-edv.de>"
__status__  = "beta"
__date__    = "08 July 2014"

__all__ = ["Converter", "Paths", "PathsFilter", "PathsExclude", "PathsShow",
        "Shields"]


import os
import sys

import logging
logging.basicConfig(format='%(levelname)s:%(name)s:line %(lineno)s: %(message)s')
log = logging.getLogger(__name__)

try:
    from rsbactools import config, converter, rsbac
except ImportError as error:
    print(error)
    sys.exit(-1)

# Path where ff config files located
RSBAC_FF_CONFIG_DIR = "/etc/rsbac/ff"
# maps given keywords form ff config to a class
RSBAC_FF_CLASS_MAPPER = {
    "paths": "Paths",
    "paths-exclude": "PathsExclude",
}
# internal values for module FF to display readable values
RSBAC_FF_FLAGS  = {
    "1": "read_only",
    "2": "execute_only",
    "4": "search_only",
    "8": "write_only",
    "16": "secure_delete",
    "32": "no_execute",
    "64": "no_delete_or_rename",
    "128": "add_inherited",
    "256": "append_only",
    "512":  "no_mount",
    "1024": "no_search",
}
RSBAC_FF_ADD_INHERITED = 128
RSBAC_FF_READ_ONLY = 1

# a approximatly counter of policies
POLICY_COUNTER = 0

def update_counter(file_dir_list=False):
    global POLICY_COUNTER
    if file_dir_list:
        POLICY_COUNTER += len(file_dir_list)
    else:
        POLICY_COUNTER += 1

def get_counter():
    return POLICY_COUNTER


class Converter(object):
    """RSBAC ff_flags has a special output values.
    This Converter prepare the output and add human readable ff_flags values
    to the output.
    """

    def __init__(self, output):
        """Expect rsbac output off
            /proc: Rückgabewert: 128
            /bin: Rückgabewert: 128
        """
        self.output = output

    def prepare_output(self):
        """Transform the output always to a list."""
        # list comprehension does first split by line 
        # after split by space
        output = [x.split(" ") for x in self.output.split("\n") if len(x) > 0]
        try:
            # list comprehension return clean value for path 
            # by removing last sing ':'
            # and the ff_flags value
            self.output = [[x[0][:-1], x[1][:-1], x[2]] for x in output]
        except IndexError as error:
            # dont change anything
            self.output = list(output)

    def convert_output(self):
        """Transform the output to dict, on error just display them."""
        result = {}
        for i in self.output:
            if len(i) != 3:
                log.error(i)
                continue
            try:
                ff_list = converter.Converter().int_to_bin(i[2], 32)
            except IndexError as error:
                log.error(error)
                continue
            try:
                # full up dict where path is the key
                result[i[0]] = {
                    "ff_flags": i[2],
                    "ff_list": [(RSBAC_FF_FLAGS[str(x)], x) for x in ff_list]
                }
            except KeyError as error:
                log.error(i)
                log.error("Value not in RSBAC_FF_FLAGS: %s" % error)
        self.output = result

    def convert(self):
        """Return a mixed."""
        self.prepare_output()
        self.convert_output()
        return self.output


class PathsShow(object):

    def format_result(self, result):
        """Print the formated output."""
        output = Converter(result).convert()
        if not output:
            return
        for path, value in sorted(output.items()):
            if len(value["ff_list"]) == 1:
                print("%-54s%-20s% +4s" % (path, value["ff_list"][0][0], 
                    value["ff_list"][0][1]))
                continue
            print("%-54s%-20s% +4s" % (path, "", value["ff_flags"]))
            for j in range(len(value["ff_list"])):
                print("%-54s%-20s% +4s" % ("", value["ff_list"][j][0],
                    value["ff_list"][j][1]))


class Paths(object):
    """Handle the config key paths."""

    def __init__(self, policies):
        """Argument policies must be a dicts with keyword paths."""
        self.policies = policies["paths"]
        self.args = ["FF", "FD", "ff_flags"] 

    def on(self):
        try:
            for file_dir, ff_flags in self.policies.items():
                args = list(self.args +  [str(ff_flags), file_dir])
                result, error = rsbac.Rsbac().attr_set_fd(args)
                if error:
                    log.error(result)
                else:
                    update_counter()
            return True                        
        except KeyError as error:
            log.error(error)
            return False

    def off(self):
        try:
            for file_dir in self.policies.keys():
                args = list(self.args + [str(RSBAC_FF_ADD_INHERITED), file_dir])
                result, error = rsbac.Rsbac().attr_set_fd(args)
                if error:
                    log.error(result)
                else:
                    update_counter()
            return True
        except KeyError as error:
            log.error(error)
            return False

    def show(self):
        try:
            for file_dir in sorted(self.policies.keys()):
                args = list(self.args + [file_dir])
                result, error = rsbac.Rsbac().attr_get_fd(args)
                if error:
                    log.error(result)
                else:
                    update_counter()
                    PathsShow().format_result(result)
            return True
        except KeyError as error:
            log.error(error)
            return False


class PathsFilter(object):
    """Filter out exclude and exculde-startswitht from file_ dir list"""

    def __init__(self, policies):
        self.policies = policies
         
    def get_paths(self):
        """return a list"""
        return self.policies.keys()

    def get_exclude(self, path):
        """return a list"""
        if "exclude" in self.policies[path]:
            if len(self.policies[path]["exclude"]) > 0:
                return self.policies[path]["exclude"]
        return []

    def get_exclude_startswith(self, path):
        """return a list"""
        if "exclude-startswith" in self.policies[path]:
            if len(self.policies[path]["exclude-startswith"]) > 0:
                return self.policies[path]["exclude-startswith"]
        return []

    def filter_exclude(self, list_to_filter, exclude):
        """return a list"""
        return list(set(list_to_filter) - set(exclude))
    
    def filter_exclude_startswith(self, list_to_filter, exclude):   
        result = list_to_filter
        for i in sorted(list_to_filter):
            for j in exclude:
                if i.startswith(j):
                    result.remove(i)
                    break
        return result

    def get_filtered_list(self):
        """return a list"""
        result = []
        for path in self.get_paths():
            try:
                list_to_filter = os.listdir(path)
            except OSError as error:
                log.error(error)
                continue
            if self.get_exclude(path):
                list_to_filter = self.filter_exclude(list_to_filter,
                    self.get_exclude(path))
            if self.get_exclude_startswith(path):
                list_to_filer = self.filter_exclude_startswith(list_to_filter,
                    self.get_exclude_startswith(path))
            result.extend([os.path.join(path, x) for x in list_to_filter])
        return result


class PathsExclude(object):
    """Handle the config key paths-exclude."""

    def __init__(self, policies):
        """Argument policies must be a dicts with keyword paths-exclude."""
        self.policies = policies["paths-exclude"]
        self.args = ["FF", "FD", "ff_flags"] 

    def on(self):
        try:
            file_dir_list = PathsFilter(self.policies).get_filtered_list()
            args = self.args
            args.append(str(RSBAC_FF_READ_ONLY))
            args.extend(file_dir_list)
            result, error = rsbac.Rsbac().attr_set_fd(args)
            if error:
                log.error(result)
            else:
                update_counter(file_dir_list)
            return True                        
        except KeyError as error:
            log.error(error)
            return False

    def off(self):
        try:
            file_dir_list = PathsFilter(self.policies).get_filtered_list()
            args = self.args
            args.append(str(RSBAC_FF_ADD_INHERITED))
            args.extend(file_dir_list)
            result, error = rsbac.Rsbac().attr_set_fd(args)
            if error:
                log.error(result)
            else:
                update_counter(file_dir_list)
            return True
        except KeyError as error:
            log.error(error)
            return False

    def show(self):
        try:
            file_dir_list = PathsFilter(self.policies).get_filtered_list()
            args = self.args
            args.extend(file_dir_list)
            result, error = rsbac.Rsbac().attr_get_fd(args)
            if error:
                log.error(result)
            else:
                update_counter(file_dir_list)
                PathsShow().format_result(result)
            return True
        except KeyError as error:
            log.error(error)
            return False


class Shields(object):

    def __init__(self):
        self.args = {}
        self.policies = {}

    def add_args(self, args):
        for key, value in args.items():
            self.args[key.replace("_", "-")] = value

    def set_log_level(self, log_level):
        log.setLevel(log_level)

    def get_log_level(self):
        return log.getEffectiveLevel()

    def update_policies(self, config_file):
        """"""
        log.debug("loading config: %s" % config_file)
        jl = config.JsonLoader()
        jl.set_log_level(self.get_log_level())
        if jl.add_config(config_file) and jl.load_config():
            log.debug("add policies values")
            self.policies.update(jl.get_values())
            return True
        else:
            return False

    def get_policies(self, key=False):
        try:
            if key and key.startswith("@"):
                return {}
            elif key:
                log.debug("Found key in policies: %s" % key)
                return self.policies[key]
            else:
                return self.policies
        except KeyError as error:
            log.debug("Skip key is not in policies: %s" % key)
            return False

    def load_configs(self, config_dir):
        try:
            for config_file in sorted(os.listdir(config_dir)):
                if config_file.endswith(".json"):
                    self.update_policies(os.path.join(config_dir, config_file))
            return True
        except OSError as error:
            log.warning(error)
            return False
   
    def run(self):
        # set all keys to status off full
        if self.args["full"]:
            for key in self.get_policies().keys():
                self.args[key] = self.args["full"]

        for key in self.args.keys():
            if not self.get_policies(key):
                continue
            if not self.args[key]:
                continue
            for i in self.get_policies(key).keys():
                try:
                    log.debug("call: %s()" % RSBAC_FF_CLASS_MAPPER[i])
                    obj = getattr(sys.modules[__name__], 
                        RSBAC_FF_CLASS_MAPPER[i])(self.get_policies(key))
                except KeyError as error:
                    log.debug(error)
                    log.debug("No class mapper found for: %s" % i)
                    continue
                try:
                    log.debug("call: %s()" % self.args[key])
                    getattr(obj, self.args[key])()
                except TypeError as error:
                    log.debug("failed: %s()" % self.args[key])
                    log.debug(error)
                    return False
        return True

    def get_policies_counter(self):
        return get_counter() 
    
