#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

class SMSTeknikError(Exception):
    pass

class AccessDenied(SMSTeknikError):
    pass

class ParseError(SMSTeknikError):
    pass

class EmptyMessage(SMSTeknikError):
    pass

class NoSMSLeft(SMSTeknikError):
    pass

class InvalidPhonenumber(SMSTeknikError):
    pass

class BlockedNumber(SMSTeknikError):
    pass
