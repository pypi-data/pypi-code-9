from copy import deepcopy
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory
from plone.app.testing import login
from plone.app.testing import TEST_USER_NAME
from collective.compoundcriterion.testing import IntegrationTestCase


TEXT_TO_FIND = u'special_text_to_find'
DOCUMENT_COMMON_TEXT = u'My_document_common_text'
COMPOUND_QUERY = [{
    'i': 'CompoundCriterion',
    'o': 'plone.app.querystring.operation.compound.is',
    'v': 'testing-compound-adapter',
}]


class TestCriterion(IntegrationTestCase):

    def _setupSomeDocuments(self):
        '''
        '''
        portal = self.layer['portal']
        data = (
            {'id': 'document1',
             'title': 'My_document_common_title',
             'text': DOCUMENT_COMMON_TEXT},
            {'id': 'document2',
             'title': 'My_document_common_title',
             'text': DOCUMENT_COMMON_TEXT},
            {'id': 'document3',
             'title': 'My_document_common_title' + ' ' + TEXT_TO_FIND,
             'text': DOCUMENT_COMMON_TEXT},
            {'id': 'document4',
             'title': 'My document 4 title',
             'text': DOCUMENT_COMMON_TEXT},
            {'id': 'document5',
             'title': 'My_document_5_title' + ' ' + TEXT_TO_FIND,
             'text': 'My_document_NOT_common_text'},
        )
        res = []
        for document in data:
            documentId = portal.invokeFactory(id=document['id'],
                                              type_name='Document',
                                              title=document['title'],
                                              text=document['text'])
            document = getattr(portal, documentId)
            document.reindexObject()
            res.append(document)
        return res

    def test_criterion(self):
        """
          Check that the compound criterion is taken into account :
          - add some documents with various title, including document with a
            special_text_to_find;
          - add a collection and check if it returns the wished elements.
        """
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        # setup some documents
        document1, document2, document3, document4, document5 = self._setupSomeDocuments()

        # add a collection using the compound criterion
        portal.invokeFactory("Collection",
                             "collection",
                             title="Collection",
                             query=COMPOUND_QUERY,
                             sort_on='getId')
        collection = portal['collection']
        results = collection.results(batch=False)
        # document3 and document5 are found
        self.assertTrue(results.actual_result_count == 2)
        self.assertTrue(results[0].UID == document3.UID())
        self.assertTrue(results[1].UID == document5.UID())

    def test_works_with_other_criteria(self):
        '''
          Check that it does work together with other criterion selected on the collection.
          The com
        '''
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        # setup some documents
        document1, document2, document3, document4, document5 = self._setupSomeDocuments()

        # compound criterion restrict to doc3 and doc5
        # the additional criterion here will restrict to documents
        # having DOCUMENT_COMMON_TEXT in SearchableText, so doc1, doc2, doc3 and doc4
        # the result will be the intersection of both, so only document3 will be found
        query = COMPOUND_QUERY + [{
            'i': 'SearchableText',
            'o': 'plone.app.querystring.operation.string.is',
            'v': DOCUMENT_COMMON_TEXT
        }]

        # add a collection using the compound criterion
        portal.invokeFactory("Collection",
                             "collection",
                             title="Collection",
                             query=query,
                             sort_on='getId')

        collection = portal['collection']
        results = collection.results(batch=False)
        # only document3 is found
        self.assertTrue(results.actual_result_count == 1)
        self.assertTrue(results[0].UID == document3.UID())

    def test_adapter_not_found(self):
        """
          If named adapter given to criterion does not exist, it does not break,
          it is simply not taken into account.
        """
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        # setup some documents
        document1, document2, document3, document4, document5 = self._setupSomeDocuments()

        # use a non existing named adapter
        query = deepcopy(COMPOUND_QUERY)
        query[0]['v'] = 'unexisting-named-adapter'
        query = query + [{
            'i': 'portal_type',
            'o': 'plone.app.querystring.operation.string.is',
            'v': 'Document'
        }]

        # add a collection using the compound criterion
        portal.invokeFactory("Collection",
                             "collection",
                             title="Collection",
                             query=query,
                             sort_on='getId')
        collection = portal['collection']
        results = collection.results(batch=False)
        # the compound part is not taken into account, it will return the 5 documents
        self.assertTrue(results.actual_result_count == 5)

    def test_vocabulary(self):
        """
          Test the vocabulary that display available named adapters that
          provides the ICompoundCriterionFilter interface.
        """
        factory = queryUtility(IVocabularyFactory, u'collective.compoundcriterion.Filters')
        vocab = factory(self.portal)
        # we have 3 registered adapters
        self.assertTrue(len(vocab) == 3)
        # check that returned adapters are the correct ones
        self.assertTrue('sample-compound-adapter' in vocab.by_value)
        self.assertTrue('testing-compound-adapter' in vocab.by_value)
        self.assertTrue('wrongformat-compound-adapter' in vocab.by_value)

    def test_wrong_query_format(self):
        """
          The format of the query returned by the named adapter must
          be compliant with what is generated by plone.app.querystring,
          so for example, something like :
          {
           'portal_type':
           {'query': ['portal_type1', 'portal_type2']},
           'created':
           {'query': DateTime('2015/05/05'),
            'range': 'min'},
          }
          It needs the values to be in a dict in the 'query' key.
        """
        login(self.portal, TEST_USER_NAME)
        # add a collection using the wrongformat compound criterion
        query = deepcopy(COMPOUND_QUERY)
        query[0]['v'] = 'wrongformat-compound-adapter'
        self.portal.invokeFactory("Collection",
                                  "collection",
                                  title="Collection",
                                  query=query,
                                  sort_on='getId')
        collection = self.portal['collection']
        self.assertRaises(ValueError, collection.results, batch=False)
