from __future__ import absolute_import

"""metapub.MedGenFetcher -- tools to deal with NCBI's E-utilities interface to the MedGen db"""

from lxml import etree

from .eutils_common import get_eutils_client, get_cache_path
from .exceptions import MetaPubError
from .medgenconcept import MedGenConcept
from .base import Borg, parse_elink_response
from .config import DEFAULT_EMAIL

class MedGenFetcher(Borg):
    '''MedGenFetcher (a Borg singleton object)

    An interaction layer for querying to return MedGenConcept objects.
    
    Currently available methods: eutils

    Basic Usage:

        fetch = MedGenFetcher()
    
    To specify a service method (more coming soon):

        fetch = MedGenFetcher('eutils')

    To return a MedGenConcept from a known UID:

        concept = fetch.concept_by_uid(known_UID)

    To return a list of UIDs relevant to a given term known in medgen:

        uids = fetch.uids_by_term(some_term)

    To get a medgen UID given a known Concept ID (cui):

        uid = fetch.uid_for_cui(known_cui)
    '''

    _cache_filename = 'medgen-cache.db'

    def __init__(self, method='eutils', email=DEFAULT_EMAIL, cachedir='default'):
        Borg.__init__(self)
        self.method = method
        self._cache_path = None

        if method=='eutils':
            self._cache_path = get_cache_path(cachedir, self._cache_filename)
            self.qs = get_eutils_client(self._cache_path, email=email) 
            self.uids_by_term = self._eutils_uids_by_term
            self.concept_by_uid = self._eutils_concept_by_uid
            self.concept_by_cui = self._eutils_concept_by_cui
            self.uid_for_cui = self._eutils_uid_for_cui
            self.pubmeds_for_uid = self._eutils_pubmeds_for_uid
            self.pubmeds_for_cui = self._eutils_pubmeds_for_cui
        else:
            raise NotImplementedError('coming soon: fetch from local medgen via medgen-mysql.')

    def _eutils_uids_by_term(self, term):
        '''wraps results of an medgen efetch term lookup, returning IDs of related MedGenConcepts.
        
        :return: list of medgen uids (strings)
        '''
        # http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=medgen&term=OCRL
        result = self.qs.esearch( { 'db': 'medgen', 'term': term } )
        dom = etree.fromstring(result)
        uids = []
        idlist = dom.find('IdList')
        for item in idlist.findall('Id'):
            uids.append(item.text.strip())
        return uids
    
    def _eutils_uid_for_cui(self, cui):
        '''given a ConceptID (cui), return a medgen ID.'''
        #http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=medgen&term=C0000039
        if not cui.startswith('C'):
            raise MetaPubError('Invalid CUID: must start with C (e.g. C0000039)')

        result = self.qs.esearch( { 'db': 'medgen', 'term': cui } )
        root = etree.fromstring(result).getroottree()
        try:
            uid = root.find('IdList').find('Id').text.strip()
        except AttributeError:
            raise MetaPubError('Invalid CUID: did not return MedGen id.')
        return uid

    def _eutils_concept_by_uid(self, uid):
        # http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=medgen&id=336867
        '''Returns MedGenConcept result of lookup of medgen uid. 
        
        :param uid: (string or int) medgen uid
        :return: MedGenConcept object
        '''
        uid = str(uid)
        result = self.qs.esummary( { 'db': 'medgen', 'id': uid } )
        return MedGenConcept(result)

    def _eutils_concept_by_cui(self, cui):
        '''Returns MedGenConcept result of lookup of CUI. 
        
        :param uid: (string) Concept id (CUI)
        :return: MedGenConcept object
        '''
        uid = self._eutils_uid_for_cui(cui)
        return self._eutils_concept_by_uid(uid)


    def _eutils_pubmeds_for_uid(self, uid):
        response = self.qs.elink( { 'dbfrom': 'medgen', 'id': uid, 'db': 'pubmed'} )
        ids = parse_elink_response(response)
        return ids

    def _eutils_pubmeds_for_cui(self, cui):
        '''given a ConceptID (cui), return a list of related pubmed article IDs.'''
        uid = self._eutils_uid_for_cui(cui)
        return self._eutils_pubmeds_for_uid(uid)

