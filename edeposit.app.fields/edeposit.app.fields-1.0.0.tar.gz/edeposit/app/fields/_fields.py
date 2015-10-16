# -*- coding: utf-8 -*-
from zope.interface import classImplements
from zope.interface import implementer
from zope.interface import Interface
from zope.interface.interfaces import IInterface
from zope.interface.interfaces import IMethod
from zope.schema import ValidationError

from zope.schema import ASCIILine
from .interfaces import IISBNLine
from .utils import is_valid_isbn

class WrongFormatOfISBN(ValidationError):
    __doc__ = u"""Špatný formát ISBN"""

@implementer(IISBNLine)
class ISBNLine(ASCIILine):
    def _validate(self,value):
        if not is_valid_isbn(value):
            raise WrongFormatOfISBN(value)
