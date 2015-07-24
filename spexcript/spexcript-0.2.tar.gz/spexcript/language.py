# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 19:49:28 2013

This module defines different languages for the layout/typesetting of
a script. The goal is to separate language specifics from output formats.

@author: Koos Zevenhoven
"""

from __future__ import unicode_literals, print_function, division


class Finnish:
    """Defines language-specifics of a script style."""
    
    INTERMISSION = "VÄLIAIKA"
    SCRIPT = "Käsikirjoitus"
    CHARACTERS = "Henkilöt"
    LIST_OF_SCENES = "Kohtausluettelo"
    TITLE = "Otsikko"
    DATE = "Päiväys"
    OWNER_OF_COPY = "Tämän kappaleen omistaja: "
    SLOGAN = "hyvä -- ei kämäinen."
    EXTRA = r"Pian Spe$\chi$cript 0.2!"
    
    @staticmethod
    def act_title(number, title):
        if title != "":
            return "%d. Näytös -- %s" % (number, title)
        else:
            return "%d. Näytös" % number
    
    @staticmethod
    def scene_title(n_act, n_scene, title):
        if title != "":
            return "Kohtaus %d.%d: %s" % (n_act, n_scene, title)
        else:
            return "Kohtaus %d.%d" % (n_act, n_scene)
    
    
    LATEX_PREAMBLE = "\\frenchspacing\n\\usepackage[finnish]{babel}"

    