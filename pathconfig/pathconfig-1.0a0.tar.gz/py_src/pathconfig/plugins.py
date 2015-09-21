#!/usr/bin/env python
# (c) 2006-2013 Yannick Versley / University of Tuebingen
# (c) 2015 Yannick Versley / University of Heidelberg
## Licensed under the Apache License, Version 2.0 (the "License"); you may
## not use this file except in compliance with the License.  You may obtain
## a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
## WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
## License for the specific language governing permissions and limitations
## under the License.

import pkg_resources

def list_plugins(category):
    '''returns a list of all plugin names for that category'''
    return sorted([x.name for x in pkg_resources.iter_entry_points(category)])

def plugin_decorator(f):
    '''decorator that makes a factory out of a function'''
    return lambda: f


def load_plugin(category, name, aux_info=None):
    '''fetches the entry point for a plugin and calls it with the given
    aux_info'''
    func = load_simple_endpoint(category, name)
    if aux_info is None:
        return func()
    else:
        return func(aux_info)
    raise KeyError(name)

def load_simple_endpoint(category, name):
    '''fetches the entry point for a plugin and calls it with the given
    aux_info'''
    for ep in pkg_resources.iter_entry_points(category):
        if ep.name == name:
            return ep.load()
    raise KeyError(name)
