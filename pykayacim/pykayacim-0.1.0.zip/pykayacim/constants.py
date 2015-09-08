#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module contains constants for PyKayacIM.

"""

from __future__ import unicode_literals

#: The URL of the API endpoint.
KAYACIM_URL = "http://im.kayac.com/api/post/"

#: The authorization methods im.kayac.com accepts.
#:
#: "none"
#:     No authorization.
#:
#: "password"
#:     Use authorization with a password.
#:
#: "secret"
#:     Use secret key cryptosystem.
#:
KAYACIM_METHODS = ["none", "password", "secret"]

#: Encoding im.kayac.com accepts.
KAYACIM_ENCODING = "utf-8"
