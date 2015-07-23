from lucenequerybuilder import Q as LQ

from ..properties import BaseProperty
from ..validators import valid_id,DesignIDValidator
from ..exceptions import DocNotFoundError,QueryIndexError,DocSaveError,ValidationException
from ..query import QueryManager
from ..utils import get_doc_type


def get_declared_variables(bases, attrs):
    properties = {}
    f_update = properties.update
    attrs_pop = attrs.pop
    for variable_name, obj in attrs.items():
        if isinstance(obj, BaseProperty):
            f_update({variable_name:attrs_pop(variable_name)})
        
    for base in bases:
        if hasattr(base, '_base_properties'):
            if len(base._base_properties) > 0:
                f_update(base._base_properties)
    return properties


class DeclarativeVariablesMetaclass(type):
    """
    Partially ripped off from Django's forms.
    http://code.djangoproject.com/browser/django/trunk/django/forms/forms.py
    """
    def __new__(cls, name, bases, attrs):
        attrs['_base_properties'] = get_declared_variables(bases, attrs)
        new_class = super(DeclarativeVariablesMetaclass,
            cls).__new__(cls, name, bases, attrs)

        return new_class

class BaseDocument(object):
    """
    Base class for all CloudantDB Documents classes.
    """       
    Q = LQ

    def __init__(self,**kwargs):
        self._raw_doc = kwargs
        self._doc = dict()
        for key,prop in self._base_properties.iteritems():
            raw_value = self._raw_doc.get(key) or prop.get_default_value()
            try:
                #Before adding value to self._doc validate it and if it doesn't 
                #validate pass. 
                prop.validate(raw_value,key)
                self._doc[key] = prop.get_python_value(raw_value)
            except ValidationException:
                pass
        if self._raw_doc.has_key('_id'):
            doc_id = self._raw_doc.get('_id')
            doc_rev = self._raw_doc.get('_rev')
            self._doc['_id'] = valid_id(doc_id)
            self._doc['_rev'] = doc_rev
            self.id = valid_id(doc_id)
            self._id = self.id
            self.pk = self.id
            self._rev = doc_rev
        
    def __getattr__(self,name):
        attr_value = self._doc.get(name)
        if not attr_value:
            if name in self._base_properties.keys():
                return ''
            else:
                raise AttributeError("'{0}' object has no attribute '{1}'".format(
                    self.__class__,name))
        return attr_value
    
    def __setattr__(self,name,value):
        if name in self._base_properties.keys():
            self._doc[name] = value
        else:
            super(BaseDocument,self).__setattr__(name,value)
        
    def save(self):
        doc = self._doc.copy()
        for key,prop in self._base_properties.iteritems():
            raw_value = doc.get(key) or prop.get_default_value()
            prop.validate(raw_value,key)
            value = prop.get_db_value(raw_value)
            doc[key] = value
            
        doc['doc_type'] = get_doc_type(self.__class__)
        
        db = self.get_db()
        resp = db.post(params=doc).json()
        if resp.has_key('error'):
            raise DocSaveError(resp.get('reason'))
        self._doc = doc
        self._doc.update(dict(_id=resp.get('id'),_rev=resp.get('rev')),
                         id=resp.get('id'))
        return self
       
    @classmethod
    def get_db(cls):
        raise NotImplementedError
    
    @classmethod
    def register_single_index(cls,index):
        db = cls.get_db()
        resp = db.post('_index',params=index).json()
        if resp.get('result') != 'created':
            
            raise QueryIndexError('Your query was not indexed.')
    
    @classmethod
    def force_doc_type(cls,index):
        fields = index.get('index',dict()).get('fields',list())
        if not 'doc_type' in fields:
            fields.append('doc_type')
            index['index']['fields'] = fields
        return index
    
    @classmethod
    def register_query_index(cls,index):
        if not isinstance(index, (set,list,tuple,dict)):
            raise ValueError(
                'The index argument should be a dict, set, list, or tuple object')
        if isinstance(index, dict):
            cls.register_single_index(index)
        else:
            for i in index:
                cls.register_single_index(i)                
        return True
        
    @classmethod
    def register_index(cls,doc):
        db = cls.get_db()
        if not isinstance(doc, dict):
            raise ValueError('The index argument should be a dict object')
        if not '_id' in doc.keys():
            raise DocSaveError('All design docs need to specify an initial _id attribute')
        v = DesignIDValidator()
        v.validate(doc['_id'])
        resp = db.post(params=doc).json()
        return resp
    
    @classmethod
    def register_indexes(cls):
        try:
            cls.register_query_index({
            "index": {"fields": ["doc_type"] },
            "name" : "doc-type-index","type" : "json"
            })
        except QueryIndexError:
            pass
        
        for i in cls.Meta.cql_indexes:
            try:
                cls.register_query_index(i)
            except QueryIndexError:
                print(u"An error occured processing index: {0}".format(i.get('name')))
        for i in cls.Meta.design_indexes:
            cls.register_index(i)
            
    @classmethod
    def objects(cls):
        return QueryManager(cls)
            
    @classmethod    
    def get(cls,doc_id):
        db = cls.get_db()
        doc = db.document(doc_id).get().json()
        if doc.has_key('error'):
            raise DocNotFoundError(doc.get('reason'))
        else:
            return cls(**doc)
    
    def delete(self):
        doc_id = self._doc['_id']
        db = self.get_db()
        doc = db.document(doc_id)
        doc_attrs = doc.get().json()
        rev = doc_attrs['_rev']
        doc.delete(rev)  
    
    class Meta:
        use_db = 'default'
        cql_indexes = []
        design_indexes = []
        
        
class Document(BaseDocument):
    __metaclass__ = DeclarativeVariablesMetaclass 