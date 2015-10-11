# -*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright (c) 2015 Thorsten Simons (sw@snomis.de)
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import sys
import os.path
import time


# initialized needed variables
#
class Gvars:
    """
    Holds constants and variables that need to be present within the
    whole project.
    """

    # version control
    s_version = "2.0.2"
    s_build = "{}/Sm" \
        .format(time.strftime('%Y-%m-%d', time.localtime()))
    s_minPython = "3.4.0"
    s_description = "hcplogs"
    s_dependencies = ['hcpsdk']

    # constants
    Version = "v.{} ({})".format(s_version, s_build)
    Description = 'HCP access log collector'
    Author = "Thorsten Simons"
    AuthorMail = "sw@snomis.de"
    AuthorCorp = ""
    AppURL = ""
    License = "MIT"
    Executable = "hcplogs"


class Ivars:
    """
    Holds variables needed for initialization tasks
    """
    args = None
    statuspollrate = 30  # default value for status poll
