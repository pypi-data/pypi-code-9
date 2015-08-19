#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from collections import namedtuple


# Functions & classes =========================================================
class ConversionRequest(namedtuple("ConversionRequest", ["marc_xml",
                                                         "uuid",
                                                         "url"])):
    """
    Request to convert MARC XML to MODS.

    Attributes:
        marc_xml (str): Which MARC XML you wish to convert to MODS.
        uuid (str): UUID for given MARC XML.
        url (str): URL of the resource in edeposit (private or not).
    """
