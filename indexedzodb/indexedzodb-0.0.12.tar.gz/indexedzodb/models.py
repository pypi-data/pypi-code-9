import uuid

import ZODB
import persistent
import BTrees
import transaction

from repoze.catalog.catalog import Catalog
from repoze.catalog.query import Eq, Gt, Lt, Ge, Le, Contains, DoesNotContain, NotEq, Any, NotAny
from repoze.catalog.indexes.field import CatalogFieldIndex


class DoesNotExist(Exception):
    pass


class NoIndex(Exception):
    pass


class ZODBModel(persistent.Persistent):
    _id = None
    _v_reindex = False

    class Meta:
        table = "zodbmodel"
        index_fields = ()

    def __init__(self, *args, **kwargs):
        for key in kwargs:
            value = kwargs[key]
            if hasattr(self, key):
                setattr(self, key, value)

    @classmethod
    def _get_index_fields(cls):
        try:
            return cls.Meta.index_fields
        except AttributeError:
            return ()

    @classmethod
    def _get_connection(cls):
        try:
            return cls.Meta.connection
        except AttributeError:
            zodb = ZODB.DB(None)
            cls.Meta.connection = zodb.open()
            return cls.Meta.connection

    @classmethod
    def _get_model_root(cls):
        root = cls._get_connection().root
        if not hasattr(root, cls.Meta.table):
            model_root = BTrees.OOBTree.BTree()
            setattr(root, cls.Meta.table, model_root)
            model_root['objects'] = BTrees.OOBTree.BTree()
            model_root['catalog'] = Catalog()
            model_root['catalog_index'] = None

        model_root = getattr(root, cls.Meta.table)
        # Regenerate index fields?
        if 'catalog_index' not in model_root or model_root['catalog_index'] != cls._get_index_fields():
            catalog = Catalog()
            for field in cls._get_index_fields():
                catalog[field] = CatalogFieldIndex(field)

            model_root['catalog'] = catalog
            model_root['catalog_index'] = cls._get_index_fields()

            cls.commit()
            cls.index()

        return model_root

    @classmethod
    def index(cls):
        root = cls._get_root()
        catalog = cls._get_catalog()
        for key in root:
            obj = root[key]
            try:
                catalog.reindex_doc(key, obj)
            except TypeError:
                pass

        cls.commit()

    @classmethod
    def _get_root(cls):
        model_root = cls._get_model_root()
        return model_root['objects']

    @classmethod
    def _get_catalog(cls):
        model_root = cls._get_model_root()
        if 'catalog' not in model_root:
            model_root['catalog'] = Catalog()
        return model_root['catalog']

    @classmethod
    def select(cls, attempt=0, sort_index=None, reverse=False, limit=None, *args, **kwargs):
        catalog = cls._get_catalog()
        qo = None

        for key in kwargs:
            key_parts = key.split('__', 1)
            original_key = key

            key = key_parts[0]
            if key not in catalog.keys():
                print catalog.keys()
                raise NoIndex('The field %s is not in the list of indexed fields for %s' % (key, cls.__name__))
            value = kwargs[original_key]

            if isinstance(value, ZODBModel):
                value = unicode(value)

            if len(key_parts) == 2:
                if key_parts[1] == 'gt':
                    nqo = Gt(key, value)
                elif key_parts[1] == 'lt':
                    nqo = Lt(key, value)
                elif key_parts[1] == 'gte':
                    nqo = Ge(key, value)
                elif key_parts[1] == 'lte':
                    nqo = Le(key, value)
                elif key_parts[1] == 'contains':
                    nqo = Contains(key, value)
                elif key_parts[1] == 'ncontains':
                    nqo = DoesNotContain(key, value)
                elif key_parts[1] == 'ne':
                    nqo = NotEq(key, value)
                elif key_parts[1] == 'in':
                    nqo = Any(key, value)
                elif key_parts[1] == 'nin':
                    nqo = NotAny(key, value)
                else:
                    raise Exception("Unknown comparator %s" % (key_parts[1]))
            else:
                nqo = Eq(key, value)

            if qo:
                qo = qo & nqo
            else:
                qo = nqo

        root = cls._get_root()
        if qo:
            _, results = catalog.query(qo, sort_index=sort_index, reverse=reverse, limit=limit)
        else:
            _, results = catalog.sort_result(root.keys(), sort_index=sort_index, reverse=reverse, limit=limit)

        try:
            return [root[x] for x in results]
        except KeyError, e:
            if attempt < 2:
                cls.index()
                return cls.select(attempt=attempt + 1, *args, **kwargs)
            raise e

    @classmethod
    def count(cls, *args, **kwargs):
        if len(kwargs) == 0:
            return len(cls._get_root())
        return len(cls.select(*args, **kwargs))

    @classmethod
    def get(cls, *args, **kwargs):
        if '_id' in kwargs:
            try:
                return cls._get_root()[kwargs['_id']]
            except Exception:
                raise DoesNotExist()
        try:
            return cls.select(*args, **kwargs)[0]
        except IndexError:
            raise DoesNotExist()

    def _get_safe_key(self, root):
        try:
            key = root.maxKey() + 1
        except ValueError:
            key = 1
        return key

    @classmethod
    def commit(cls):
        transaction.commit()
        cls._get_connection().sync()

    def save(self, commit=True):
        root = self._get_root()
        if not self._id:
            self._id = self._get_safe_key(root)
        root[self._id] = self

        # Check catalog fields
        for field in self._get_index_fields():
            val = getattr(self, field)
            if val is None:
                setattr(self, field, '')

        catalog = self._get_catalog()
        catalog.reindex_doc(self._id, self)

        if commit:
            transaction.commit()

    def delete(self, commit=True):
        root = self._get_root()
        if self._id:
            catalog = self._get_catalog()
            catalog.unindex_doc(self._id)

            del root[self._id]
            self._id = None

        if commit:
            transaction.commit()

    def getPk(self):
        return self._id

    def __str__(self, *args, **kwargs):
        return str(self.getPk())

    def __unicode__(self, *args, **kwargs):
        return unicode(self.getPk())

    def __setattr__(self, name, value):
        if isinstance(value, ZODBModel):
            value = unicode(value)

        persistent.Persistent.__setattr__(self, name, value)
