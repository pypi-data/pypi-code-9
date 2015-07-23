#!/usr/bin/env python
#
# Copyright (C) 2014 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Original code can be found here: https://android.googlesource.com/tools/repo/
# This is a refactor for the OpenStack project with an upgrade to Python 3.
# All code changes will be marked.
# Formatting changed to meet PEP8 requirements.

from __future__ import print_function
import imp
# from importlib import machinery, util
import os


def WrapperPath():
    return os.path.join(os.path.dirname(__file__), 'andromeda')


_wrapper_module = None

# updated to account for deprecation of the imp library.
def Wrapper():
    global _wrapper_module
    if not _wrapper_module:
        # loader = machinery.SourceFileLoader('wrapper', WrapperPath())
        # spec = machinery.ModuleSpec('wrapper', loader, origin='wrapper')
        # _wrapper_module = util.find_spec(spec)
        _wrapper_module = imp.load_source('wrapper', WrapperPath())
    return _wrapper_module
