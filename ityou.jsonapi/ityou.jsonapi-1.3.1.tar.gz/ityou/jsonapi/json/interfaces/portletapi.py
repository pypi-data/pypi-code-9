# -*- coding: utf-8 -*-
from zope.interface import Interface

#Version: 0.3
"""
Json Schnittstelle für die grafische Darstellung des Contents in Plone
"""
#get-chart-data
#
# EINE AUSWAHL VON VERSCHIEDENEN LÖSUNGSANSÄTZEN 
#

#INTERFACE VORSCHLAG

class IDisplayContent:   # eventuell umbenennen ? 
    """
    Bereitstellung von Funktionen zum Abfragen von Contentinformationen
    für die grafische Darstellung in einem Portlet
    IContent ist schon in der Plone API View vergeben.
    Display steht für die Funktion der Klasse. 
    """
    
    def __call__(self):
        """
        Nimmt Requests entgegen und leitet sie an die Methoden weiter. 
        """    
        
    def __count_content(**params): # außer funktion
        """
        Über **params wird ein Dictionary für die Catalog Suche übergeben
        
        return anzahl der ergebnisse der Catalog Suche
        
        """

    def __count_in_percent_content(**params):  # außer funktion
        """
        Über **params wird ein Dictionary für die Catalog Suche übergeben
        
        Die Anzahl der Suchergebnisse wird in ein Verhältnis von allen Objekten des Ordners gesetzt. 
        
        Die Rückgabe ist der prozentuale Anteil der Suche zum gesamten Ordner
        
        """
        
    def chart_gradient_pie_portaltype(): #http://bl.ocks.org/NPashaP/9999786
        """
        Spezielle Grafik Methoden werden mit dem Präfix 'chart' gekennzeichnet 
        
        Bei Aufruf der Funktion wird die prozentuale Zusammenstellung der portaltypes des Contextes
        in json Formatierung zurückgegeben. 
        
        Warum ? 
        Da die Daten für die Grafik schon Serverseitig zusammengestellt werden sollen, und nicht im Browser
        muss das auf die Grafik zugeschnittene Json Format als Antwort an den Browser geschickt werden.
        
        """
    
    def chart_gradient_pie_status(): #http://bl.ocks.org/NPashaP/9999786
        """
        Spezielle Grafik Methoden werden mit dem Präfix 'chart' gekennzeichnet 
        
        Bei Aufruf der Funktion wird die prozentuale Zusammenstellung der stati des Contextes
        in json Formatierung zurückgegeben. 
        
        Warum ? 
        Da die Daten für die Grafik schon Serverseitig zusammengestellt werden sollen, und nicht im Browser
        muss das auf die Grafik zugeschnittene Json Format als Antwort an den Browser geschickt werden.
        
        """
    
    
    
