# -*- coding: utf8 -*-
"""
Created on Sun Jun 29 03:15:20 2014
Updated on Tue Jul 04 11:22:00 2015
@author: Kyunghoon Kim
"""
import urllib
import urllib2
import json

def analyzer(s, url, key, nounlist=[], comp=0):
    """
    Korean Morpheme Analyzer.
    Get the JSON type result using Web API
    The function name 'Umorpheme' is an abbreviation of UNIST_morpheme
    :param s: Input Sentence
    :param key: Personal Verification Key
    :param nounlist: CUSTOM Noun list
    :param comp: Compound noun 1:True, 0:False
    :return: term order, data, feature
    at UNIST Mathematical Sciences 2014.
    """
    if 'information.center' in url:
        # Connection URL
        if url[-1] == '/':
            url = url[:-1]
        url = url+"?s=&sc="
        r = url+key

        # Custom Nouns
        if nounlist != []:
            params = urllib.urlencode({'nounlist': nounlist, 's':s})
        else:
            params = urllib.urlencode({'s':s})

        # Composition Nouns
        if comp != 0:
            r = r + "&comp="+str(comp)

        # Request
        req = urllib2.Request(r, params)
        response = urllib2.urlopen(req)
        result = json.loads(unicode(response.read()))
        return result

    else:
        """Preparing for Local Analyzer(Docker)"""
        return 'requesting...'