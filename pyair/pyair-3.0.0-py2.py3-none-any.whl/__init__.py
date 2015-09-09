#!/usr/bin/python
# -*- coding: UTF-8 -*-


import date
import reg
import stats
import xair


__version__ = "3.0.0"
__author__ = "Lionel Roubeyrie"
__email__ = "lroubeyrie@limair.asso.fr"
__all__ = ['date', 'reg', 'stats', 'xair']
__license__ = "GPL"
__changes__ = {
    '3.0.0': u"""- Separation des modules en packages distincts : pyair, pyair_utils
    - Nettoyage des fichiers pour etre conforme avec PEP8
    - ajout de xair.indice_et_ssi pour récupérer les sous-indices et les polluants faisant l'indice global""",
    '2.2': u""" - Ajout de utils.pivotCSV2 permettant de pivoter des données en gardant certaines lignes et/ou colonnes;
     - xair.XAIR.liste_campagnes : tri des campagnes par date début par défaut;
     - ajouts de sites_from_df et sites_from_csv au module geo"""
}
