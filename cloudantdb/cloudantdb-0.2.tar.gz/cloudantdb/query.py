from .exceptions import QueryError
from .utils import get_doc_type

REPR_OUTPUT_SIZE = 20

class QuerySetMixin(object):
    query_type = None

    def __init__(self,doc_class,q=None,parent_q=None):
        self.parent_q=parent_q
        self._result_cache = None
        self._doc_class = doc_class
        self.q = q
        self.evaluated = False
        self._db = self._doc_class.get_db()
        if q and parent_q:
            self.q = self.combine_qs()

    def combine_qs(self):
        raise NotImplementedError    

    def __len__(self):
        self._fetch_all()
        return len(self._result_cache)
           
    def __repr__(self):
        data = list(self[:REPR_OUTPUT_SIZE + 1])
        if len(data) > REPR_OUTPUT_SIZE:
            data[-1] = "...(remaining elements truncated)..."
        return repr(data)   
    
    def __iter__(self):
        self._fetch_all()
        return iter(self._result_cache)
    
    def _fetch_all(self):
        if self._result_cache is None:
            self._result_cache = list(self.evaluate())
        
    def count(self):
        return len(list(self.evaluate()))
        

    def delete(self):
        doc_set = self.evaluate()
        doc_ids = [{'_id':i._id,'_rev':i._rev,'_deleted':True} for i in doc_set]
        return self._db.bulk_docs(*doc_ids)
            
    def __nonzero__(self):
        self._fetch_all()
        return bool(self._result_cache)
    
    def __getitem__(self,index):
        if self._result_cache is not None:
            return self._result_cache[index]
        else:
            self._fetch_all()
            return self._result_cache[index]
    
    def evaluate(self):
        raise NotImplementedError
    
    def view(self,name):
        pass

def combine_list(a,b):
    if isinstance(a,(set,tuple,list)):
        a = list(a)
    else:
        a = [a]
    if isinstance(b,(set,tuple,list)):
        b = list(b)
    else:
        b = [b]
    a.extend(b)
    return a

def combine_dicts(a, b, op=combine_list):
    z = a.copy()
    z.update(b)
    z.update([(k, op(a[k], b[k])) for k in set(b) & set(a)])
    return z
    
    
class QuerySet(QuerySetMixin):
    
    def __init__(self, doc_class,q=None, parent_q=None, fields=None, 
        skip=None, limit=None, sort_by=None,read_quorum=None,model_map=None):
        self._skip = skip
        self._limit = limit
        self._read_quorum = read_quorum
        self.fields = fields
        self._sort_by = sort_by
        self.model_map = model_map
        super(QuerySet,self).__init__(doc_class,q=q,parent_q=parent_q)
        
    def find(self,q):
        return QuerySet(self._doc_class,self.force_doc_type_query(q),self.q,
            fields=self.fields,skip=self._skip,limit=self._limit,
            sort_by=self._sort_by,read_quorum=self._read_quorum)
    
    def force_doc_type_query(self,q):
        q['doc_type'] = get_doc_type(self._doc_class)
        return q
    
    def all(self):
        
        return QuerySet(self._doc_class,
            #All queryset
            self.force_doc_type_query({"_id": {"$gt": 0}}),
            self.q,
            fields=self.fields,skip=self._skip,limit=self._limit,
            sort_by=self._sort_by,read_quorum=self._read_quorum
            )
        
    def combine_qs(self):
        return combine_dicts(self.parent_q, self.q)
        
    def evaluate(self):
        qs = dict(selector=self.q)
        if isinstance(self.fields, list):
            qs['fields'] = self.fields
        if self._limit:
            qs['limit'] = self._limit
        if self._sort_by:
            qs['sort'] = self._sort_by
        if self._read_quorum:
            qs['r'] = self._read_quorum
        if self._skip:
            qs['skip'] = self._skip
        
        self._query_dict = qs
        resp = self._db.post('_find',params=qs)
        json_data = resp.json()
        error = json_data.get('error',None) 
        docs = json_data.get('docs',None)
        if error:
            raise QueryError(json_data.get('reason'))
        if docs:
            
            if self.model_map is None:
                doc_set = [self._doc_class(**i) for i in docs]
            else:
                parent_doc_type = get_doc_type(self._doc_class)
                for i in docs:
                    doc_type = i.get('doc_type',parent_doc_type)
                    if doc_type == parent_doc_type:
                        self._doc_class(**i)
        else:
            doc_set = []
        return doc_set
    
    def fields_list(self,fields):
        return QuerySet(self._doc_class,self.q,self.parent_q,
            fields=fields,skip=self._skip,limit=self._limit,
            sort_by=self._sort_by,read_quorum=self._read_quorum)
    
    def limit(self,no_docs):
        return QuerySet(self._doc_class,self.q,self.parent_q,
            fields=self.fields,skip=self._skip,limit=no_docs,
            sort_by=self._sort_by,read_quorum=self._read_quorum)
    
    def skip(self,no_docs):
        return QuerySet(self._doc_class,self.q,self.parent_q,
            fields=self.fields,skip=no_docs,limit=self._limit,
            sort_by=self._sort_by,read_quorum=self._read_quorum)
    
    def sort_by(self,fields_dict):
        return QuerySet(self._doc_class,self.q,self.parent_q,
            fields=self.fields,skip=self._skip,limit=self._limit,
            sort_by=fields_dict,read_quorum=self._read_quorum)
    
    def read_quorum(self,no_replicas):
        return QuerySet(self._doc_class,self.q,self.parent_q,
            fields=self.fields,skip=self._skip,limit=self._limit,
            sort_by=self._sort_by,read_quorum=no_replicas)
    
class SearchSet(QuerySetMixin):
    
    def __init__(self, doc_class,index_id=None,index_name=None,q=None, parent_q=None,include_docs=True):
        self._index_id = index_id
        self._index_name = index_name
        self._include_docs = include_docs
        super(SearchSet,self).__init__(doc_class,q,parent_q)
        
    def __call__(self,index_id,index_name,q,include_docs=True):
        return SearchSet(self._doc_class,index_id=index_id,
                         index_name=index_name,q=q,include_docs=include_docs)
        
    def combine_qs(self):
        if self.q and self.parent_q:
            return self.parent_q & self.q    
        return self.q
             
    def search(self,q,include_docs=True):
        return SearchSet(self._doc_class,self._index_id,
                         self._index_name,self.q,self.parent_q,include_docs)
    
    def evaluate(self):
        doc = dict(query=self.q,include_docs=self._include_docs)
        resp = self._db.get('_design/{0}/_search/{1}'.format(
                            self._index_id,self._index_name),params=doc)
        json_data = resp.json()

        error = json_data.get('error',None) 
        docs = json_data.get('rows',None)
        
        if error:
            raise QueryError(json_data.get('reason'))
        if doc:
            doc_set = list()
            for i in docs:
                if not self._include_docs:
                    i['fields']['_id'] = i.pop('id')
                    doc_set.append(self._doc_class(**i['fields']))
                else:
                    doc_set.append(self._doc_class(**i['doc']))
            return doc_set
        else:
            return doc_set
        
    
class QueryManager(object):
    
    def __init__(self,cls):
        self._doc_class = cls
        
        self.find = QuerySet(self._doc_class).find
        self.all = QuerySet(self._doc_class).all
        self.search = SearchSet(self._doc_class)