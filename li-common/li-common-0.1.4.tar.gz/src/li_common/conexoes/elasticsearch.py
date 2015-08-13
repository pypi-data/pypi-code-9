from li_common.helpers import tente_outra_vez

from pyelasticsearch import ElasticSearch
from requests import ConnectionError

# Existe apenas para repasse de exceptions via heranca
from pyelasticsearch import exceptions as ElasticsearchExceptions

class ElasticsearchConnect(object):
    def __init__(self,elasticsearch_url):
        self.server = ElasticSearch(elasticsearch_url)

    def search(self, query, **kwargs):
        return self.server.search(query, **kwargs)

    @tente_outra_vez(ConnectionError, tentativas=4, tempo_espera=3, multiplicador_espera=2)
    def index(self, index, content_type, content):
        return self.server.index(index, content_type, content)

    def bulk_index(self, index, doc_type, docs, **kwargs):
        return self.server.bulk_index(index, doc_type, docs, **kwargs)

    def delete_by_query(self, index, doc_type, **kwargs):
        return self.server.delete_by_query(index, doc_type, **kwargs)

    def delete(self, index, doc_type, id, **kwargs):
        return self.server.delete(index, doc_type, id, **kwargs)