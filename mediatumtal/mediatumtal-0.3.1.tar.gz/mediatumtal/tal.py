# -*- coding: utf-8 -*-
'''
Created on 26.07.2013
@author: stenzel
'''
from __future__ import division, absolute_import
from mediatumtal import talextracted
from mediatumtal.talextracted import processTAL, str_processTAL
from mediatumtal.talextracted import runTAL  # @UnusedImport


def str_getTAL(page, context, macro=None, language=None, request=None):
    return str_processTAL(context, file=page, macro=macro, language=language, request=request)

def getTAL(page, context, macro=None, language=None, request=None):
    return processTAL(context, file=page, macro=macro, language=language, request=request)

def getTALstr(string, context, macro=None, language=None, mode=None):
    return processTAL(context, string=string, macro=macro, language=language, mode=mode)


def set_base(basedir):
    talextracted.setBase(basedir)


def add_translator(translator):
    talextracted.addTranslator(translator)


def add_macro_resolver(macroresolver):
    talextracted.addMacroResolver(macroresolver)


def add_template_globals(**kwargs):
    """Adds globals from a dict which will be available in all template contexts"""
    talextracted.template_globals.update(kwargs)