# encoding: utf-8
import sys
import os
import types
import datetime
import inspect
import traceback
import urllib.request
import urllib
from http import *
import http.client
import json
import yaml
import uuid
import re
from collections import *
from weakref import proxy as _proxy
from time import *
import base64
import copy
import logging
from logging import debug as debug
from pprint import pprint as pp
http.client.HTTPConnection.debuglevel = 0


# Subclass this class if you need to
# overwrite __getitem__ and have it
# called
# when accessing slices.
# If you subclass list directly,
# __getitem__ won't get called when
# accessing
# slices as in mylist[2:4].
class UserListSubclass(list):

    def __getslice__(self, i, j):
        return self.__getitem__(slice(i, j))

    def __setslice__(self, i, j, seq):
        return self.__setitem__(slice(i, j), seq)

    def __delslice__(self, i, j):
        return self.__delitem__(slice(i, j))


def doc_representer(dumper, data):
    items = data.items()
    return dumper.represent_mapping('tag:yaml.org,2002:map', items)

yaml.add_representer(OrderedDict, doc_representer)


class Server(dict, MutableMapping):

    def __init__(self, base, username, password):
        self.base = base
        self.username = username
        self.password = password
        self.resource = Resource(base, username, password)
        dbs = self.resource.get('_all_dbs')
        d = {}
        for key in dbs:
            d[key] = Database(self, key)
        dict.__init__(self, d)

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)

    def __getitem__(self, name):
        return dict.__getitem__(self, name)

    setdefault = MutableMapping.setdefault
    update = MutableMapping.update

    def create(self, dbname):
        res = self.resource.put(dbname)

    def delete(self, dbname):
        self.resource.delete(dbname)

    def replicate(self, source, target):
        self.resource.put(target)
        params = json.dumps({'source': source, 'target': target})
        self.resource.post('_replicate', params)


class magic_doc(dict):

    def __init__(self, db):
        self.db = db

    def __xgetattr__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        else:
            raise AttributeError

    def update_completer_dict(self, attr):
        params = {
            'startkey': '"' + attr + '"',
            'endkey': '"' + attr + '\uffff"',
            'group': 'true'}
        self.db.magic = False
        res = self.db.view_full('app/ids', params)
        self.db.magic = True
        if len(res['rows']) == 1:
            self[res['rows'][0]['key']] = self.db[res['rows'][0]['key']]
        else:
            for row in res['rows']:
                title = row['key']
                num = row['value']
                self[title] = 'please select an unique key'


class Database(dict, MutableMapping):

    def __init__(self, server, dbname):
        self.db = dbname
        self.base = server.base
        uri = self.base
        # activate magic functions (return Documents instead of raw data)
        self.magic = True
        self.resource = server.resource
        self.translate = 0
        self.translatemode = 1
        self.filter_count = 0
        self.filter_requests = dict()
        self.docs = magic_doc(self)

    def __hash__(self):
        return id(self)

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)

    def merge(self, a, b):
        """Merge two deep dicts non-destructively
    Uses a stack to avoid maximum recursion depth exceptions
    >>> a = {'a': 1, 'b': {1: 1, 2: 2}, 'd': 6}
    >>> b = {'c': 3, 'b': {2: 7}, 'd': {'z': [1, 2, 3]}}
    >>> c = merge(a, b)
    >>> from pprint import pprint; pprint(c)
    {'a': 1, 'b': {1: 1, 2: 7}, 'c': 3, 'd': {'z': [1, 2, 3]}}
    """
        assert self.quacks_like_dict(a), self.self.quacks_like_dict(b)
        dst = a.copy()
        stack = [(dst, b)]
        while stack:
            current_dst, current_src = stack.pop()
            for key in current_src:
                if key not in current_dst:
                    current_dst[key] = current_src[key]
                else:
                    if (
                        self.quacks_like_dict(current_src[key]) and
                        self.quacks_like_dict(current_dst[key])
                    ):
                        stack.append((current_dst[key], current_src[key]))
                    else:
                        current_dst[key] = current_src[key]
        return dst

    def merge_blank(self, a, b):
        """Merge two deep dicts non-destructively
    Uses a stack to avoid maximum recursion depth exceptions
    >>> a = {'a': 1, 'b': {1: 1, 2: 2}, 'd': 6}
    >>> b = {'c': 3, 'b': {2: 7}, 'd': {'z': [1, 2, 3]}}
    >>> c = merge(a, b)
    >>> from pprint import pprint; pprint(c)
    {'a': 1, 'b': {1: 1, 2: 7}, 'c': 3, 'd': {'z': [1, 2, 3]}}
    """
        assert self.quacks_like_dict(a), self.self.quacks_like_dict(b)
        dst = a.copy()
        stack = [(dst, b)]
        while stack:
            current_dst, current_src = stack.pop()
            for key in current_dst:
                if key not in current_src:
                    current_dst[key] = ''
                else:
                    if (
                        self.quacks_like_dict(current_src[key]) and
                        self.quacks_like_dict(current_dst[key])
                    ):
                        stack.append((current_dst[key], current_src[key]))
                    else:
                        current_dst[key] = current_src[key]
        return dst

    def quacks_like_dict(self, object):
        """Check if object is dict-like"""
        return isinstance(object, Mapping)

    def __getitem__(self, obj):
        language = None
        parts = obj.split('/')
        if len(parts) > 1:
            obj = parts[0]
            language = parts[1]
        resultdoc = None
        if self.translatemode == 0 and language is not None:
            doc = self.resource.getordered('/'.join([self.db, obj]))
            path = '/'.join([self.db, obj, language])
            translatedoc = self.resource.getordered(path)

            resultdoc = self.merge_blank(doc, translatedoc)
        elif self.translatemode == 0 or language is None:
            resultdoc = self.resource.getordered('/'.join([self.db, obj]))
        elif self.translatemode == 1:
            doc = self.resource.getordered('/'.join([self.db, obj]))
            translatedoc = None
            try:
                if language in doc['_attachments']:
                    path = '/'.join([self.db, obj, language])
                    translatedoc = self.resource.getordered(path)
            except Exception as e:
                debug(e)
                pass
            if translatedoc is not None:
                resultdoc = self.merge(doc, translatedoc)
        resultdoc = self.convert(resultdoc)
        return resultdoc

    def getAll(self):
        return self.resource.get('/'.join([self.db, '_all_docs']))['rows']

    def getDesignDoc(self, name):
        return self.convert(self.resource.get(
            '/'.join([self.db, '_design/', name])))

    def getDesignDocs(self):
        return self.resource.get(
            '/'.join([self.db, '_all_docs?startkey="_design/"&endkey="_design0"&include_docs=true']))['rows']

    def dump(self, backupdir):
        path = '/'.join([self.db, '_all_docs?include_docs=true'])
        docs = self.resource.get(path)['rows']
        for item in docs:
            doc = item['doc']
            jsondoc = json.dumps(doc, sort_keys=True)
            filename = os.path.join(backupdir, doc['_id']) + '.json'
            with open(filename, 'w') as f:
                f.write(jsondoc)

    def new_from_type(self, origobj):
        if '@context' in origobj:
            obj = origobj['@context']
        else:
            obj = origobj
        if '@extends' in origobj:
            parent_obj = self.new(origobj['@extends'])
            print('extends!')
            print(parent_obj)
            print(obj)
            obj['@type'] = origobj['_id']
            obj = self.merge(parent_obj, obj)
            print(obj)
        leaftypes = ['str', 'int', 'bool', 'float']
        if '@type' in obj:
            fieldtype = obj['@type']
        if '@container' in obj:
            return []
        else:
            for item in obj:
                if not item.startswith('@'):
                    if isinstance(obj[item],
                                  dict) and '@container' in obj[item]:
                        obj[item] = []
                    else:
                        if isinstance(obj[item], dict):
                            if '@type' in obj[item] and obj[
                                    item]['@type'] in leaftypes:
                                if '@default' in obj[item]:
                                    obj[item] = obj[item]['@default']
                                else:
                                    obj[item] = eval(obj[item]['@type'])()
                            elif '@type' in obj[item] and ':' in obj[item]['@type']:
                                obj[item] = ''
                            else:
                                obj[item] = self.new_from_type(obj[item])
        return obj

    def new(self, doctype='doonx:base', uid=None):
        if uid is None:
            uid = uuid.uuid4().hex
        typedoc = self[doctype]
        xdoc = self.new_from_type(self[doctype])
        if doctype is not None:
            doc = Document()
            doc.merge(xdoc)
            doc['_id'] = uid
            doc['@type'] = doctype
            print("doctype %s" % doctype)
            if '@description' in doc:
                del doc['@description']
            if '@title' in doc:
                del doc['@title']
            if '_rev' in doc:
                del doc['_rev']
        return self.convert(doc)
        return doc

    def save_bulk(self, docs):
        for doc in docs:
            if isinstance(doc, Document):
                doc.deflate()
        xdoc = dict()
        xdoc['docs'] = docs
        jsondoc = json.dumps(xdoc)

        res = self.resource.post(self.db + '/_bulk_docs', jsondoc)
        return res

    def json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""
        if isinstance(obj, datetime.datetime):
            serial = obj.isoformat()
            return seria
        if isinstance(obj, datetime.date):
            serial = obj.isoformat()
            return serial

    def save(self, doc, path=None):
        if isinstance(doc, Document):
            doc.deflate()
        if path is not None and '/' in path:
            res = self.resource.put(
                self.db + '/' + path, doc, {'Content-Type': 'application/json'})
        else:
            jsondoc = json.dumps(doc, default=self.json_serial)
            res = self.resource.post(self.db, jsondoc)
        rid = res.get('id', None)
        rev = res.get('rev', None)
        return {'id': rid, 'rev': rev}

    def force_save(self, doc, path=None):
        try:
            rev = self[doc['_id'].split('/')[0]]['_rev']
            debug(rev)
            path += '?rev=' + rev
            doc['_rev'] = rev
        except Exception as e:
            debug(e)
        return self.save(doc, path)

    def delete(self, path, params=None):
        return self.resource.delete('/' + self.db + '/' + path)

    def force_delete(self, uid):
        doc = self[uid]
        res = self.delete(uid + '?rev=' + doc['_rev'])
        try:
            if 'superdocs' in doc:
                for parent in doc['superdocs']:
                    parentobj = self[parent]
                    parentobj = self.convert(parentobj)
                    for i, subpageid in enumerate(parentobj['subdocs']):
                        if subpageid == uid:
                            del parentobj['subdocs'][i]
                    # important!! dont leave the empty dict {} for subdocs,
                    # it will catch the items again via lazy loading (to be
                    # verified)
                    if len(parentobj['subdocs']) == 0:
                        del parentobj['subdocs']
                    parentobj.force_save()
        except Exception as e:
            print(e)
        return res

    def view_full(self, name, options=None):
        if not name.startswith('_'):
            design, name = name.split('/', 1)
            name = '/'.join(['_design', design, '_view', name])
        res = self.resource.get('/' + self.db + '/' + name, options)
        if self.magic:
            for i, item in enumerate(res):
                res[i] = self.convert(res[i])
        return res

    def copy(self, src, dest):
        path = '/'.join([self.db, src])
        res = self.resource.copy(path, dest)
        return res

    def iview(self, name, options=None, filter=None, filtertype='and'):
        add = {'include_docs': 'true'}
        if options is None:
            options = add
        else:
            options.update(add)
        return self.view(name, options, filter, filtertype)

    def view(
            self,
            name,
            options=None,
            select=None,
            docfilter=None,
            filtertype='and'):
        """Return documents from couchdb view
        The design documents (beginning with '_design') are not included
        """
        if isinstance(docfilter, str):
            docfilter = yaml.load(docfilter)
        res = []
        if not name.startswith('_'):
            if '/' in name:
                design, name = name.split('/', 1)
                name = '/'.join(['_design', design, '_view', name])
            else:
                design = 'app/'
                name = '/'.join(['_design', design, '_view', name])
        viewresults = self.resource.get('/'.join([self.db, name]), options)
        if 'error' in viewresults:
            return viewresults
        for item in viewresults['rows']:
            if 'doc' in item:
                viewitem = item['doc']
            else:
                viewitem = item['value']
            if viewitem['_id'].startswith('_design'):
                continue
            if docfilter is not None:
                if self.convert(viewitem).filter(
                        docfilter, filtertype=filtertype):
                    res.append(viewitem)
            else:
                res.append(viewitem)
        if select is not None:
            select = yaml.load(select)
            for i, item in enumerate(res):
                res[i] = dict()
                for key in select:
                    res[i][key] = item[key]
        if self.magic:
            for i, item in enumerate(res):
                res[i] = self.convert(res[i])
        return res

    setdefault = MutableMapping.setdefault
    update = MutableMapping.update

    def findOne(self, view, key):
        params = {'startkey': '"' + key + '"', 'endkey': '"' + key + '\uffff"'}
        return self.view(view, params)[0]

    def convert(self, obj=None, silent=True):
        if obj is not None:
            arguments = Document(obj, silent=silent, db=self)
        else:
            arguments = Document({}, silent=silent, db=self)
        return arguments


class SafeDict(dict, MutableMapping):

    def __getitem__(self, name):
        if name in self:
            return self[name]
        else:
            return list

    def __getattr__(name):
        if name in self:
            return self[name]
        else:
            return list


class _Link(object):
    __slots__ = 'prev', 'next', 'key', '__weakref__'


class DocumentProxyList(UserListSubclass):

    def __init__(
            self,
            li,
            db=None,
            silent=False,
            root=None,
            name=None,
            parent=None):
        # todo: vorher beim init und beim setitem mit documents etc. füllen und nicht im nachhinein immer wieder documents
        # erstellen
        self._db = db
        self._root = root
        self._name = name
        self._silent = silent
        self._parent = parent
        for i, item in enumerate(li):
            if isinstance(li[i], dict):
                li[i] = Document(
                    li[i],
                    root=self._root,
                    db=self._db,
                    silent=self._silent)
            elif isinstance(li[i], list):
                li[i] = DocumentProxyList(
                    li[i], root=self._root, db=self._db, silent=self._silent)
        super().__init__(li)

    def __setitem__(self, index, value):
        if isinstance(value, dict):
            item = Document(
                value,
                root=self._root,
                db=self._db,
                silent=self._silent)
        if isinstance(value, list):
            item = DocumentProxyList(
                value,
                root=self._root,
                db=self._db,
                silent=self._silent)
        if not (isinstance(value, dict) or isinstance(value, list)):
            if len(str(value)) == 32:
                try:
                    item = Document(
                        self._db[
                            str(value)],
                        root=self._root,
                        db=self._db,
                        silent=self._silent)
                except Exception as e:
                    debug(e)
        super().__setitem__(index, item)

    def __getitem__(self, index):
        r = super().__getitem__(index)
        # hier wird bei jedem erneuten abfragen des verknüpften
        # Objekts wieder ein neues Document erstellt und zurückgegeben. Das
        # kann den Anwender verwirren, da er Properties setzt und beim erneuten
        # abfragen des Objektes (sofern es nicht gespeichert wurde), das alte
        # Objekt aus der Datenbank bekommt.
        # Lösung: nur beim init und setitem ein Konversion vornehmen und danach
        # nur noch die items pur zurückgeben (super.getitem)
        if len(str(r)) == 32:
            try:
                doc = Document(
                    self._db[
                        str(r)],
                    root=self._root,
                    db=self._db,
                    silent=self._silent)
                # daher wird hier explizit das Document über setitem gesetzt
                self.__setitem__(doc)
                return doc
            except:
                return r
        return r

    def getSilent(self):
        return self._silent

    def load(self):
        li = list()
        for item in self:
            li.append(Document(self._db[str(item)]))
        return li

    def process(self, item):
        if isinstance(item, list) and not isinstance(item, DocumentProxyList):
            return DocumentProxyList(
                item,
                root=self._root,
                db=self._db,
                silent=self._silent,
                name=self._name)
        if isinstance(item, dict):
            return Document(
                item,
                root=self._root,
                db=self._db,
                silent=self._silent)

        doc = item
        # if len(str(item))==32:
        #    try:
        #        doc = Document(self._db[str(item)], silent=self.getSilent(), root=self._root, db=self._db)
        #    except Exception as e:
        #        #debug(e)
        #        doc = item
        return doc

    def __iter__(self):
        for item in self:
            yield self.process(item)

    def _meta(self, item):
        try:
            if not item.startswith('@'):
                item = '@' + item
            return self._root.get('@type')['@context'][self._name][item]
        except Exception as e:
            debug(e)
            return None

    def native(self):
        l = list(self)
        for i, item in enumerate(l):
            if isinstance(
                    l[i], Document) or isinstance(
                    l[i], DocumentLeafMixin):
                l[i] = l[i].native()
        return l


class DocumentLeafMixin():

    def __new__(cls, value, name=None, root=None, parent=None):
        return super(DocumentLeafMixin, cls).__new__(cls, value)

    def __init__(self, value, name=None, root=None, parent=None):
        print('d1')
        super().__init__()
        self._name = name
        self._root = root
        self._parent = parent

    def _meta(self, item):
        print('? x ' * 70)
        labels = {
            "_id": "ID",
            "_rev": "Revision",
            "@type": "Type"
        }
        if (item == 'label' or item == '@label') and self._name in labels.keys():
            return labels[self._name]
        try:
            if not item.startswith('@'):
                item = '@' + item
            return self._root.get('@type')[self._name][item]
        except Exception as e:
            debug(e)
            return None

    def _get_path(self):
        return self._parent._get_path([self._name])

    def span(self):
        return '<span itemprop="%s">%s</span>' % (self._name, self)

    def email(self):
        return '<a href="mailto:%s">%s</a>' % (self, self)

    def image(self):
        return '<img src="%s" />' % self

    def input(self):
        return '<input name="%s" value="%s" />' % (self._name, self)

    def create(self):
        output = """
           <label for="">%s</label>

        """ % ()
        return output

    def native(self):
        if isinstance(self, str):
            return str(self)
        if isinstance(self, int):
            return int(self)
        if isinstance(self, float):
            return float(self)
        if isinstance(self, bool):
            return bool(self)


class IntLeaf(int, DocumentLeafMixin):

    def __new__(cls, value, name=None, root=None, parent=None):
        return super(IntLeaf, cls).__new__(cls, value)

    def __init__(self, value, name=None, root=None, parent=None):
        super().__init__(value, name, root, parent)


class FloatLeaf(float, DocumentLeafMixin):

    def __new__(cls, value, name=None, root=None, parent=None):
        return super(FloatLeaf, cls).__new__(cls, value)

    def __init__(self, value, name=None, root=None, parent=None):
        super().__init__(value, name, root, parent)


class StrLeaf(str, DocumentLeafMixin):

    def __new__(cls, value, name=None, root=None, parent=None):
        return super(StrLeaf, cls).__new__(cls, value)

    def __init__(self, value, name=None, root=None, parent=None):
        super().__init__(value, name, root, parent)


class BoolLeaf(int, DocumentLeafMixin):

    def __new__(cls, value, name=None, root=None, parent=None):
        return super(BoolLeaf, cls).__new__(cls, value)

    def __init__(self, value, name=None, root=None, parent=None):
        super().__init__(value, name, root, parent)

    def __bool__(self):
        if self == 0:
            return False
        else:
            return True


class nil(object):

    def __init__(self, obj):
        self._obj = obj

    def __bool__(self):
        return False

    def __len__(self):
        return 0

    def __str__(self):
        return ''

    def __getattr__(self, attr):
        return nil(self._obj)

    def __call__(self):
        return nil(self.obj)

    def __iter__(self):
        for item in range(0):
            yield False


class Document(OrderedDict):

    def __init__(
            self,
            indict=None,
            root=None,
            db=None,
            silent=False,
            name=None,
            parent=None):
        # defaultvalues for pagetype, todo: implement a more generic system of default and
        # override values
        self.__dict__['__oditems'] = OrderedDict().__dict__
        super(self.__class__, self).__init__()
        self._inited = True
        self._db = db
        self._silent = silent
        self._name = name
        self._parent = parent
        if root is not None:
            self._root = root
        else:
            self._root = self
        if indict is not None:
            for item in indict:
                if isinstance(item, tuple):
                    item, value = item
                else:
                    try:
                        value = indict[item]
                    except Exception as e:
                        pass
                self.__setitem__(item, self.pack_item(item, value))
        if indict is not None and '@type' in indict and indict[
                '@type'] == 'doonx:page':
            if 'stylesheets' not in indict:
                self.__setitem__('stylesheets', [])
            if 'scripts' not in indict:
                self.__setitem__('scripts', [])

    def __hash__(self):
        if '_id' in self:
            debug(self['_id'])
            debug(hash(self['_id']))
            return hash(self['_id'])
        else:
            return id(self)

    def __repr__(self):
        res = 'Document('
        resitems = list()
        for item in self:
            resitems.append('%s: %s' % (item, self[item]))
        res += ', '.join(resitems)
        return res + ')\n'

    def _get_path(self, path):
        if self._parent is None:
            return path
        if self._parent == self._root:
            return path.append(self._name)
        else:
            return self._parent._get_path(path.append(self._name))

    def __setitem__(self, key, value):
        value = self.pack_item(key, value)
        # to be removed, if not working
        self.__dict__[key] = value
        super(self.__class__, self).__setitem__(key, value)

    def __getitem__(self, item):
        try:
            if not isinstance(item, list):
                value = super().__getitem__(item)
                return value
            else:
                key = item[0]
                target = super().__getitem__(key)
                if len(item) > 2:
                    newitem = item[1:]
                elif len(item) == 2:
                    newitem = item[1]
                else:
                    newitem is None
                return target[newitem]
        except:
            raise KeyError

    def __getattr__(self, item):
        if item in self.__dict__['__oditems']:
            if item in self.__dict__:
                return self.__dict__[item]
            else:
                raise AttributeError
        else:

            try:
                return self.__dict__[item]
            except Exception as e:
                pass
            try:
                value = self.__getitem__(item)
                return value
            except Exception as e:
                # debug(e)
                pass
            try:
                return self.__dict__[item]
            except Exception as e:
                # debug(e)
                if '_inited' in self.__dict__ and self.__dict__[
                        '_inited'] == True:
                    return nil({})
            od = OrderedDict()
            if item in self.__dict__['__oditems']:
                raise AttributeError

    def __setattr__(self, key, value):
        if key in self.__dict__['__oditems']:
            self.__dict__[key] = value
        else:
            internal = [
                '_root',
                '_inited',
                '_db',
                '_silent',
                '__oditems',
                '_parent',
                '_name']
            if key in internal:
                self.__dict__[key] = value
            else:
                self.__setitem__(key, value)

    def _data(self):
        for item in self:
            if not (item.startswith('@') or item.startswith('_')):
                yield item

    def load(self, item):
        value = super().__getitem__(self, item)
        if isinstance(value, list):
            li = list()
            for item in value:
                li.append(Document(self._db[str(item)]))
            return li
        else:
            return Document(self._db[str(item)])

    def save(self):
        deflated = self.deflate()
        out = self._db.convert(deflated)
        id, rev = self._db.save(out.native())
        return 'ok'

    def deflate(self):
        def deflate_walk(obj, firstlevel=False):
            if isinstance(
                    obj,
                    Document) and not firstlevel and '_id' in obj:
                # print(obj)
                return obj['_id']
            elif isinstance(obj, list):
                res = list()
                for item in obj:
                    res.append(deflate_walk(item))
                return res
            elif isinstance(obj, dict):
                res = OrderedDict()
                for item in obj:
                    res[item] = deflate_walk(obj[item])
                return res
            return obj
        return deflate_walk(self, firstlevel=True)

    def force_save(self):
        try:
            self['_rev'] = self._db[self['_id']]['_rev']
        except Exception as e:
            debug(e)
        self.save()
        return 'ok'

    def _meta(self, item, attr):
        labels = {
            "_id": "ID",
            "_rev": "Revision",
            "@type": "Type"
        }
        if item in labels:
            return labels[item]
        try:
            if not attr.startswith('@'):
                attr = '@' + attr
            return self.get('@type')['@context'][item][attr]
        except Exception as e:
            debug('Meta attribute not found: ' + str(e))
            return ''

    def _span(self, item):
        return '<span itemprop="%s">%s</span>' % (item, self.__getitem__(item))

    def _email(self, item):
        return '<a href="mailto:%s">%s</a>' % (item, self.__getitem__(item))

    def _image(self, item):
        return '<img src="%s" />' % (item, self.__getitem__(item))

    def _input(self, item):
        return '<input type="text" name="%s" value="%s" />' % (
            item, self.__getitem__(item))

    def _checkbox(self, item):
        if item not in self._ordering or self.__getitem__(
                item) in ['None', 'False', 'false', '0']:
            checked = ''
        else:
            checked = ' checked="checked"'
        return '<input type="checkbox" name="%s" %s />' % (item, checked)

    def _type(self):
        return self['@type'].replace(':', '_')

    def pack_item(self, key, value):
        if isinstance(value, dict) and not isinstance(value, Document):
            packed_item = Document(
                value,
                root=self._root,
                db=self._db,
                silent=self._silent,
                name=key,
                parent=self)
        elif isinstance(value, list) and not isinstance(value, DocumentProxyList):
            packed_item = DocumentProxyList(
                value,
                root=self._root,
                db=self._db,
                silent=self._silent,
                name=key,
                parent=self)
        else:
            if isinstance(value, str):
                packed_item = StrLeaf(
                    value, name=key, root=self._root, parent=self)
            elif isinstance(value, int):
                packed_item = IntLeaf(
                    value, name=key, root=self._root, parent=self)
            elif isinstance(value, float):
                packed_item = FloatLeaf(
                    value, name=key, root=self._root, parent=self)
            elif isinstance(value, bool):
                packed_item = BoolLeaf(
                    value, name=key, root=self._root, parent=self)
            else:
                packed_item = value
        return packed_item

    def merge(self, b):
        a = self
        dst = a
        stack = [(dst, b)]
        while stack:
            current_dst, current_src = stack.pop()
            for key in current_src:
                if key not in current_dst:
                    current_dst[key] = self.pack_item(key, current_src[key])
                else:
                    if self.quacks_like_dict(
                            current_src[key]) and self.quacks_like_dict(
                            current_dst[key]):
                        stack.append((current_dst[key], current_src[key]))
                    else:
                        current_dst[key] = self.pack_item(
                            key, current_src[key])
        self = dst

    def merge_object(self, objectToMergeFrom, objectToMergeTo=None):
        """
        Used to copy properties from one object to another if there isn't a naming conflict;
        """
        if objectToMergeTo is None:
            objectToMergeTo = self
        for property in objectToMergeFrom.__dict__:
            # Check to make sure it can't be called... ie a method.
            if not callable(objectToMergeFrom.__dict__[property]):
                setattr(
                    objectToMergeTo, property, getattr(
                        objectToMergeFrom, property))

        return objectToMergeTo

    def merge_shy(self, b):
        a = self
        dst = a
        stack = [(dst, b)]
        while stack:
            current_dst, current_src = stack.pop()
            for key in current_src:
                if key not in current_dst:
                    current_dst[key] = self.pack_item(key, current_src[key])
                else:
                    if self.quacks_like_dict(
                            current_src[key]) and self.quacks_like_dict(
                            current_dst[key]):
                        stack.append((current_dst[key], current_src[key]))
        self = dst

    def select(self, selection):
        res = dict()
        for key in self.__dict__:
            if key in selection:
                res[key] = self[key]
        return res

    def from_map(self, obj, mappinglist, _util=None):
        codes = dict()
        for line in mappinglist.split('\n'):
            if len(line.strip()) == 0:
                continue
            line = line.strip()
            if line.startswith('- '):
                line = line[2:]
            else:
                raise Exception(
                    'The mapping has syntax errors. The top level must be a list.')
            if ': ' not in line:
                raise Exception(
                    'The mapping has syntax errors. Please use ": " as a divider for src and dest.')
            if '#' in line:
                mapping, code = line.split('#')
                mapping = mapping.strip()
                code = code.strip()
                src, dest = mapping.split(': ', 1)
                codes[dest] = code
        mappinglist = yaml.load(mappinglist)
        for mappingitem in mappinglist:
            for item in mappingitem:
                selector = item
                if selector == '_dummy':
                    self[mappingitem[item]] = None
                else:
                    # the commented line would be nicer, but then you have to keep the next print line, as the object has to be accessed, otherwise
                    # the object keeps being lazy and __dict__ is not filled
                    # dirty workaround ;-(
                    # print(obj)
                    # self[mappingitem[item]] = eval(selector, obj.__dict__)
                    self[mappingitem[item]] = getattr(obj, selector)

        # postprocess
        for item in codes:
            l = dict()
            l['parent'] = 'holla'
            parent = 'holla'
            func = eval(
                'lambda x, _util: ' +
                codes[item],
                globals(),
                globals())
            self[item] = func(self[item], _util)

    def quacks_like_dict(self, object):
        """Check if object is dict-like"""
        return isinstance(object, Mapping)

    def __xstr__(self):
        if not self._silent or doonx.debugging.active:
            # return ''.join(self._before, super().__str__(), self._after)
            return super().__str__()
        else:
            return ''

    def setSilent(self, silent=True):
        self._silent = silent

    def getSilent(self):
        return self._silent

    def get(self, item):
        # if isinstance(value, str) and (len(str(value))==32 or ((':' in value)
        # and (item!='doonx:type') and value.startswith('doonx'))) and
        # item!='_id' and item!='doonx:type':
        value = self.__getitem__(item)
        if item in self:
            try:
                doc = Document(
                    self._db[
                        str(value)],
                    root=self._root,
                    db=self._db,
                    silent=self._silent,
                    name=item,
                    parent=self)
                return doc
            except Exception as e:
                debug(e)
                doc = value
                return doc
            else:
                return value
        else:
            return None

    def to_yaml(self):
        native = self.native()
        docstr = bytes(
            yaml.dump(
                native,
                default_flow_style=False),
            'utf-8').decode('unicode_escape')
        return docstr

    def to_json(self):
        return json.dumps(self, sort_keys=False)

    def _wrap(self, wrap):
        self.__before, self.__after = wrap.split('|')

    def filter(self, docfilter=None, doc=None, filtertype='and'):
        docfilter = dict(docfilter)
        resdoc = copy.copy(dict(docfilter))
        if doc is None:
            doc = self
        for i, query in enumerate(docfilter.keys()):
            if query not in doc:
                resdoc[query] = False
            else:
                if isinstance(doc[query], dict):
                    return self.filter(
                        doc=doc[query], docfilter=docfilter[query])
                else:
                    operator = docfilter[query][0]
                    if operator not in ['<', '>', '=', '^', '$', '%']:
                        operator = '='
                        operand = docfilter[query]
                    else:
                        operand = docfilter[query][1:]
                    value = doc[query]
                    t = type(value)
                    # convert operand to type of docitem
                    operand = t(operand)
                    if operator == '<':
                        if value < operand:
                            resdoc[query] = True
                        else:
                            resdoc[query] = False
                    if operator == '>':
                        if value > operand:
                            resdoc[query] = True
                        else:
                            resdoc[query] = False
                    if operator == '=':
                        if value == operand:
                            resdoc[query] = True
                        else:
                            resdoc[query] = False
                    if operator == '!':
                        if value != operand:
                            resdoc[query] = True
                        else:
                            resdoc[query] = False
                    if operator == '^':
                        if value.startswith(operand):
                            resdoc[query] = True
                        else:
                            resdoc[query] = False
                    if operator == '$':
                        if value.endswith(operand):
                            resdoc[query] = True
                        else:
                            resdoc[query] = False
                    if operator == '%':
                        if operand in value:
                            resdoc[query] = True
                        else:
                            resdoc[query] = False
            if filtertype == 'and':
                if resdoc[query] == False:
                    return False
            if filtertype == 'or':
                if resdoc[query] == True:
                    return True
        if filtertype == 'and':
            return True
        if filtertype == 'or':
            return False

    def preprocess(self, doc, template=None):
        if doc['@type'] == 'doonx:image':
            maxthumbwidth = 80
            # maxthumbheight = 80
            if '/fe/' in template:
                maxthumbwidth = 800
                # maxthumbheight = 600
            width = None
            try:
                width = int(doc['width'].replace('px', ''))
                width = min(width, maxthumbwidth)
            except:
                width = ''
            height = None
            try:
                height = doc['height']
                height = min(width, maxthumbwidth)
            except:
                height = ''
            size = str(width) + 'x' + str(height)
            for i, image in enumerate(doc['images']):
                tempnum = uuid.uuid4().hex
                thumbfile = 'files/temp/' + tempnum + '.png'
                args = [
                    'convert',
                    '-resize',
                    size,
                    self.rootdir +
                    '/' +
                    image['url'],
                    thumbfile]
                # add check of return of following line
                subprocess.check_call(args)
                # the following line will set the thumb only in the copy of Document, which will be returned by the listproxy,
                # so changing items of that copy will not affect the original doc (everything before the brackets [] will be untouched.
                # -> think about it, if its is possible to fix and how to fix that
                # one solution would be to use another notation to access the items of a document:
                # doc.get('images',i,'thumb')
                # second solution:
                # dont return Document in the getitem function of Document, but return normal dicts etc. then it will be possible to add
                # a new key to that dict. but: if we dont return Document in
                # the getitem function, we ...
                doc['images'][i]['thumb'] = thumbfile
                o1 = doc['images'][i]
                o2 = doc['images'][i]
        return doc

    def choose_template(
            self,
            configtests,
            filetest,
            fallback=None,
            strict=False):
        if configtests is not None and configtests != list() and configtests != [
                []]:
            for configtest in configtests:
                path = os.path.join(self.rootdir, configtest)
                if os.path.exists(path):
                    return configtest
        for template in self.templates:
            for file in filetest:
                if file in template:
                    return template
        if strict:
            return fallback
        else:
            if fallback is not None:
                return fallback
            return 'default_template.html'

    def fe_render(self, dx):
        debug('~ ' * 70)
        doc = self
        filecheck = doc['@type'].replace(':', '_') + '_show'
        if filecheck in dx.config.templates.fe:
            configtest = [dx.config.templates.fe[filecheck]]
        else:
            configtest = None
        filetest = ['fe/' + doc['@type'].replace(':', '_') + '_show' + '.html']
        fallback = 'extensions/base/templates/fe/default_show.html'
        template = self.choose_template(configtest, filetest, fallback)
        debug(template)
        doc = self.preprocess(doc, template)
        return doonx.framework.Doonx.render(template, {'c': self.convert(doc)})

    def native(self):
        o = OrderedDict(self)
        for item in o:
            if isinstance(
                o[item],
                Document) or isinstance(
                o[item],
                DocumentProxyList) or isinstance(
                o[item],
                    DocumentLeafMixin):
                o[item] = o[item].native()
        return o


class Resource(object):

    def __init__(self, base, username, password, secure=False):
        self.base = base
        self.secure = secure
        s = '%s:%s' % (username, password)
        b = s.encode('utf-8')
        base64string = base64.encodebytes(b)[:-1].decode('utf-8')
        self.baseheaders = {
            'User-Agent': 'Doonx/1.0 +http://www.doonx.org/',
            'Accept': 'application/json',
            'Content-type': 'application/json'}
        self.authheader = {'Authorization': 'Basic %s' % base64string}

    def get(self, path, params=None):
        if params:
            params = urllib.parse.urlencode(params)
        if self.secure:
            protocol = 'https://'
        else:
            protocol = 'http://'
        uri = protocol + self.base + path
        uriparts = urllib.parse.urlparse(uri)
        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'User-Agent': 'ZML/1.0 +http://www.zml.org/'}

        req = urllib.request.Request(uri, params, headers)
        res = urllib.request.urlopen(req)

        # conn = http.client.HTTPConnection(self.base)
        # if params:
        #     print(path+'?'+params)
        #     conn.request('GET','/'+path+'?'+params,None,headers)
        # else:
        #     conn.request('GET','/'+path,None,headers)
        # res = conn.getresponse()
        data = res.read()
        # conn.close()
        # compresseddata=data
        # compressedstream=io.StringIO(compresseddata)
        # gzipper = gzip.GzipFile(fileobj=compressedstream)
        # data = gzipper.read()
        dbslist = data.decode("utf-8", "strict")
        # dbs=json.loads(dbslist,object_pairs_hook=OrderedDict)
        dbs = json.loads(dbslist)
        return dbs

    def getordered(self, path, params=None):
        if params:
            params = urllib.parse.urlencode(params.items())
        uri = 'http://' + self.base + path
        uriparts = urllib.parse.urlparse(uri)
        headers = {'User-Agent': 'Doonx/1.0 +http://www.doonx.org/'}
        conn = http.client.HTTPConnection(self.base)
        conn.request('GET', '/' + path, None, headers)
        res = conn.getresponse()
        data = res.read()
        conn.close()
        dbslist = data.decode("utf-8", "strict")
        dbs = json.loads(dbslist, object_pairs_hook=OrderedDict)

        if 'error' in dbs:
            raise Exception(
                'Couchdb error for document %s: %s, reason: %s' %
                (path, dbs['error'], dbs['reason']))
        return dbs

    def post(self, path='', params=None):
        conn = http.client.HTTPConnection(self.base)
        headers = dict(self.baseheaders)
        postheaders = {'Content-Length': str(len(params))}
        headers.update(self.authheader)
        headers.update(postheaders)
        conn.request("POST", '/' + path, params, headers)
        res = conn.getresponse()
        data = res.read().decode('utf-8')
        dataobj = json.loads(data)
        conn.close()
        return dataobj

    def put(self, path, body=None, headers=None):
        if headers is None:
            headers = self.authheader
        else:
            headers.update(self.authheader)
        conn = http.client.HTTPConnection(self.base)
        conn.request('PUT', '/' + path, json.dumps(body), headers)
        res = conn.getresponse()
        data = res.read().decode('utf-8')
        dataobj = json.loads(data)
        conn.close()
        return dataobj

    def copy(self, path, dest):
        conn = http.client.HTTPConnection(self.base)
        headers = dict(self.baseheaders)
        headers.update({'Destination': dest})
        conn.request("COPY", '/' + path, None, headers)
        res = conn.getresponse()
        data = res.read().decode('utf-8')
        dataobj = json.loads(data)
        conn.close()
        return dataobj

    def delete(self, path, params=None):
        if path[0] != '/':
            path = '/' + path
        conn = http.client.HTTPConnection(self.base)
        conn.request('DELETE', path, params, self.authheader)
        res = conn.getresponse()
        data = res.read().decode('utf-8')
        dataobj = json.loads(data)
        conn.close()
        return dataobj


class DefaultErrorHandler(urllib.request.HTTPDefaultErrorHandler):

    def http_error_default(self, req, fp, code, msg, headers):
        result = urllib.request.HTTPError(
            req.get_full_url(), code, msg, headers, fp)
        result.status = code
        return result


class SmartRedirectHandler(urllib.request.HTTPRedirectHandler):

    def http_error_301(self, req, fp, code, msg, headers):
        result = urllib.request.HTTPRedirectHandler.http_error_301(
            self, req, fp, code, msg, headers)
        result.status = code
        return result

    def http_error_302(self, req, fp, code, msg, headers):
        result = urllib.request.HTTPRedirectHandler.http_error_302(
            self, req, fp, code, msg, headers)
        result.status = code
        return result


class OrderedDictYAMLLoader(yaml.Loader):
    """
    A YAML loader that loads mappings into ordered dictionaries.
    """

    def __init__(self, *args, **kwargs):
        yaml.Loader.__init__(self, *args, **kwargs)

        self.add_constructor(
            'tag:yaml.org,2002:map',
            type(self).construct_yaml_map)
        self.add_constructor(
            'tag:yaml.org,2002:omap',
            type(self).construct_yaml_map)

    def construct_yaml_map(self, node):
        data = OrderedDict()
        yield data
        value = self.construct_mapping(node)
        data.update(value)

    def construct_mapping(self, node, deep=False):
        if isinstance(node, yaml.MappingNode):
            self.flatten_mapping(node)
        else:
            raise yaml.constructor.ConstructorError(
                None, None, 'expected a mapping node, but found %s' %
                node.id, node.start_mark)

        mapping = OrderedDict()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                hash(key)
            except(TypeError, exc):
                raise yaml.constructor.ConstructorError(
                    'while constructing a mapping',
                    node.start_mark,
                    'found unacceptable key (%s)' %
                    exc,
                    key_node.start_mark)
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value
        return mapping


class xResource(object):
    # todo: connect this Ressource class with the Resource class in couchlayer

    def __init__(self, db=None):
        self.db = db

    exposed = True

    def GET(self):
        return 'self.db'

    def PUT(self):
        # put data into storage
        pass
