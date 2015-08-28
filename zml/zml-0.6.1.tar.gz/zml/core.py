# encoding: utf-8
import logging
import pyparsing
from pyparsing import *
import os
import html
import zml
from collections import OrderedDict
from termcolor import colored
from asteval import Interpreter
import zml.rest


aeval = Interpreter()
integer = Word(nums)
variable = Word(alphas)
arithOp = Word("+-*/", max=1)

indentobj = ZeroOrMore(Literal(' '))
indentobj.leaveWhitespace()
word = Word(printables, excludeChars="{ }")
lword = Word(printables + ' ', excludeChars="{ } < >")
descriptor = Word(printables + ' ', excludeChars=": { } < >")
attributekey = Word(printables, excludeChars=": = '")
xword = Word(printables)
nocolon = Word(printables, excludeChars=': # .')
nomoustache = Word(printables, excludeChars='{ }')
moustache_expression = Word(printables, excludeChars='{ }')
moustacheline_expression = Word(printables, excludeChars='{ }')
nomoustache.setWhitespaceChars('')
quote = Suppress("'")
uid = Suppress('#') + Word(printables, excludeChars='# : .')
cls = Suppress('.') + Word(printables, excludeChars='. : #')
classes = ZeroOrMore(cls)('classes')
classes.setParseAction(lambda tokens: " ".join(tokens))
id_classes = Optional(uid)('uid') + classes
id_classes.setParseAction(lambda res: renderIdClasses(res))
colon = Optional(':')
moustache = Suppress('{')
moustache += moustache_expression('expression')
moustache += Suppress('}')
rawmoustache = Suppress('{')
rawmoustache += moustache_expression('expression')
rawmoustache += Suppress('}')
descriptor = Word(printables, excludeChars='\. : - % *')
isComponent = indentobj('indent') + descriptor('namespace') + \
    '-' + descriptor('component')


def renderNormal(token):
    return '%s' % token


def renderMoustache(token):
    return '\'+str(' + token + ')+\''


def renderExpression(expr):
    return '\'+aeval.eval(' + expr + ')+\''


def renderMoustacheLine(res):
    res.toString = 'str(' + res.expression + ')'
    return res


def checkInlineColon(res):
    if len(res) == 0:
        res.has_colon = False
        return res
    res.has_colon = True
    if res.colon == '':
        res.has_colon = False
    return res


def checkComponent(s):
    try:
        result = isComponent.parseString(s)
    except pyparsing.ParseException as x:
        return False
    return True


def renderAttributes(res):
    if len(res) == 0:
        return ""
    return ' '.join(res)


def renderAttributeValue(*args, **kwargs):
    try:
        if len(args[0]) > 0:
            out = '+'.join(args[0])
            return "\"'+" + out + "+'\""
        else:
            return ''
    except Exception as e:
        debug('serialize Exception')
        debug(e)
        return ''


def renderAttribValue(res):
    out = res[0]
    return out


def renderIdClasses(res):
    sep = ''
    clss = ''
    uid = ''
    if res.uid:
        uid = ' id="%s" ' % res.uid[0]
        sep = ' '
    else:
        uid = ''
    if res.classes:
        clss = ' class="%s" ' % res.classes
        sep = ' '
    else:
        clss = ''
    return uid + clss


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def serialize(*args, **kwargs):
    if len(args) == 0:
        args = "''"
    try:
        if len(args[2]) == 1 and is_number(args[2][0]) and not args[
                2][0].startswith("'") and not args[2][0].endswith("'"):
            return str(args[2][0])
        med = ["'%s'" % item for item in args[2]]
        out = "+' '+".join(med)
        out = out.replace("'", "\'")
        return out
    except Exception as e:
        debug('serialize Exception')
        debug(e)
        return ''


def serialize_attributevalue(*args, **kwargs):
    try:
        if len(args[0]) > 0:
            out = '+'.join(args[2])
            return '"' + out + '"'
        else:
            return ''
    except Exception as e:
        debug('serialize Exception')
        debug(e)
        return ''


def serialize_textmoustache(*args, **kwargs):
    try:
        if len(args[0]) > 0:
            # return args[2][0]
            out = '+'.join(args[2])
            return "'" + out + "'"
        else:
            return ''
    except Exception as e:
        debug('serialize Exception')
        debug(e)
        return ''


def renderWords(*args, **kwargs):
    items = [html.escape(item) for item in args[2]]
    return items


def dataRenderWords(*args, **kwargs):
    items = [html.escape(item) for item in args[2]]
    inlinestr = "".join(args[2])
    if inlinestr == '':
        return ''
    pyobj = aeval.eval(inlinestr)
    return pyobj


def splitWords(*args, **kwargs):
    try:
        items = args[2].split()
        return items
    except Exception as e:
        debug('serialize Exception')
        debug(e)
        return ''


def renderInlineTag(tokens):
    out = "<%s%s%s>%s</%s>" % (
        tokens.name, tokens.id_classes,
        tokens.attributes, tokens.ic, tokens.name)
    return out


def renderQuotedString(*args):
    item = args[2][0]
    if item.startswith("'") and item.endswith("'"):
        item = item[1:-1]
    item = textmoustache.parseString(item)
    return item


def renderQuotedStringKeepQuotes(*args):
    item = args[2][0]
    return item


def renderFunction(*args, **kwargs):
    return '_' + args[2].funcname + '(' + ','.join(args[2].funcparams) + ')'


qs = QuotedString(quoteChar="'")
qs.setParseAction(renderQuotedString)
qskeepquotes = QuotedString(quoteChar="'", unquoteResults=False)
qskeepquotes.setParseAction(renderQuotedStringKeepQuotes)
words = OneOrMore(lword('word'))('words')
datawords = OneOrMore(lword('word'))('words') | Empty()
words_explicit = OneOrMore(lword('word'))('words')
attributewords = OneOrMore(word('word'))('words')
words.setParseAction(renderWords)
moustache.setParseAction(lambda tokens: renderMoustache(tokens[0]))
textmoustache = ZeroOrMore(moustache('moustache') | words('words'))
textmoustache.setParseAction(serialize_textmoustache)
datawords.setParseAction(dataRenderWords)
words_explicit.setParseAction(lambda tokens: " '+' ".join(tokens))
wordnoequal = Word(printables, excludeChars='=')
wordnodash = Word(printables, excludeChars='- :')
# attribvalue = rawmoustache | Word(printables + ' ', excludeChars="'")
# expression = Word(printables + ' ')
expression = Word(printables + ' ', excludeChars="'")
expression.setParseAction(lambda expr: renderExpression(expr))
# attribvalue = ZeroOrMore(qs | rawmoustache | expression)
# attribvalue = qskeepquotes | ZeroOrMore(nocolon | rawmoustache)
attribvalue = qs | ZeroOrMore(nocolon | rawmoustache)
attribvalue.setParseAction(lambda res: renderAttribValue(res))
# attrib = wordnoequal('key') + Suppress('=') + Suppress("'") + \
#    attribvalue('value') + Suppress("'")
# attrib = wordnoequal('key') + Suppress('=') + Suppress("'") + \
attrib = wordnoequal('key') + Suppress('=') + attribvalue('value')
# attributevalue = moustache | Word(printables + ' ', excludeChars="' ")
funcparam = Word(printables, excludeChars=',:)(')('funcparam')
funcparams = delimitedList(funcparam, delim=',')('funcparams')
func = Literal('_') + Word(printables, excludeChars='(=)')('funcname') + \
    Literal('(') + Optional(funcparams) + Literal(')')
func.setParseAction(renderFunction)
attributevalue = qs | func | Word(printables, excludeChars=": ")
# attributevalue = moustache | Word(printables + ' ')
attributevalue.setParseAction(lambda res: renderAttributeValue(res))
attribute = attributekey + Literal('=')
# attribute += quote + attributevalue + quote
attribute += attributevalue
attribute.setParseAction(lambda res: ''.join(res))
attributes = ZeroOrMore(attribute)
attributes.setParseAction(lambda res: renderAttributes(res))
nomoustache.setParseAction(lambda tokens: renderNormal(tokens[0]))
moustache_expression.setParseAction(
    lambda tokens: renderMoustache(tokens[0]))
moustacheline_expression.setParseAction(
    lambda tokens: renderMoustacheLine(tokens))
inlinetag = '<' + descriptor('name') + \
    id_classes('id_classes') + attributes('attributes') + \
    ': ' + ZeroOrMore(lword('ic')) + '>'
inlinetag.setParseAction(renderInlineTag)


composit = (
    Suppress(Optional("'")) +
    ZeroOrMore(
        moustache('moustache') | inlinetag('inline_tag') |
        words('words')) + Suppress(Optional("'"))) | (
    ZeroOrMore(
        moustache('moustache') |
        inlinetag('inline_tag') | nocolon('nocolon')))
inline_content = qs('words') | composit
inline_content_explicit = ZeroOrMore(
    OneOrMore(moustache('moustache')) | words_explicit)
composit.setParseAction(serialize)
inline_content_explicit.setParseAction(serialize)
inline_attributevalue = ZeroOrMore(
    OneOrMore(moustache('moustache')) | attributewords)
indentobj.setParseAction(lambda tokens: "".join(tokens))
inline_semantics = '<' + word('name') + ': ' + Optional("'") + \
    inline_content + Optional("'") + Optional(' ') + '>'
inherit_line = Suppress('#') + Suppress('inherit')
inherit_line += xword('templatefile')
namespace_line = Suppress('#') + Suppress('namespace') + \
    Word(printables, excludeChars="=")('nsid')
namespace_line += '=' + xword('namespace')
import_line = Suppress('#') + Suppress('import')
import_line += xword('module')
moustache_line = indentobj('indent') + Suppress('{')
moustache_line += moustacheline_expression('expression')
moustache_line += Suppress('}')
name = Word(printables, excludeChars='"  = : # .' + "'")
inline_attributevalue.setParseAction(serialize_attributevalue)
explicit_line = indentobj('indent')
explicit_line += inline_content_explicit('inline_content')
explicit_single_line = indentobj('indent') + Suppress('"')
explicit_single_line += inline_content_explicit('inline_content')
element = indentobj('indent') + Optional(name('name')) + \
    id_classes('id_classes')
element += attributes('attributes') + colon('colon') + Optional(' ')
element += inline_content('inline_content')
routevalue = Word(printables, excludeChars="'")
route_line = indentobj('indent') + \
    Word(printables, excludeChars=':')('key') + \
    colon('colon') + Optional(' ') + quote + routevalue('value') + quote
viewhelper = indentobj('indent') + wordnodash('namespace') + '-' + \
    wordnodash('name') + id_classes('id_classes') + \
    ZeroOrMore(Group(attrib))('attribs') + \
    Suppress(':' | Empty())
# viewhelper += ZeroOrMore(Group(attrib))('attribs')
hasInlineColon = indentobj('indent') + Optional(name('name'))
hasInlineColon += id_classes('id_classes') + attributes('attributes')
hasInlineColon += Optional(colon('colon'))
hasInlineColon += Optional(inline_content('inline_content'))
hasInlineColon.setParseAction(lambda res: checkInlineColon(res))
element_empty = indentobj('indent') + name('name')
# element_empty += id_classes('id_classes') + attributes('attributes')
element_empty += id_classes('id_classes') + attributes('attributes')
code_inline = indentobj('indent') + Suppress('%')
code_inline += ZeroOrMore(Word(printables))('code')
code_inlineblock = Suppress(Optional('<%')) + ZeroOrMore(
    Word(printables))('code') + Suppress(Optional('%>'))


class Nil(object):

    def __init__(self, obj):
        self._obj = obj

    def __bool__(self):
        return False

    def __len__(self):
        return 0

    def __str__(self):
        return ''

    def __getattr__(self, attr):
        return Nil(self._obj)

    def __call__(self):
        return Nil(self.obj)

    def __iter__(self):
        for item in range(0):
            yield False


class Node(OrderedDict):

    def __init__(self, indict=None, root=None, db=None,
                 silent=False, name=None, parent=None):
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
        if indict is not None and '@type' in indict and \
                indict['@type'] == 'zml:page':
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
        res = 'Node('
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
                        '_inited'] is True:
                    return Nil({})
            od = OrderedDict()
            if item in self.__dict__['__oditems']:
                raise AttributeError

    def __setattr__(self, key, value):
        if key in self.__dict__['__oditems']:
            self.__dict__[key] = value
        else:
            internal = ['items', '_root', '_inited', '_db',
                        '_silent', '__oditems', '_parent', '_name', '_mapping']
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
                li.append(Node(self._db[str(item)]))
            return li
        else:
            return Node(self._db[str(item)])

    def save(self):
        deflated = self.deflate()
        out = self._db.convert(deflated)
        id, rev = self._db.save(out.native())
        return True

    def deflate(self):
        def deflate_walk(obj, firstlevel=False):
            if isinstance(obj, Node) and firstlevel is False and '_id' in obj:
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
        return True

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
            return self.get('@type')['@localcontext'][item][attr]
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
        if isinstance(value, dict) and not isinstance(value, Node):
            packed_item = Node(value, root=self._root, db=self._db,
                               silent=self._silent, name=key, parent=self)
        elif isinstance(value, list) and not isinstance(value, NodeProxyList):
            packed_item = NodeProxyList(
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
        Used to copy properties from one object to another
        if there isn't a naming conflict;
        """
        if objectToMergeTo is None:
            objectToMergeTo = self
        for property in objectToMergeFrom.__dict__:
            # Check to make sure it can't be called... ie a method.
            if not callable(objectToMergeFrom.__dict__[property]):
                setattr(objectToMergeTo, property, getattr(
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
                    'The mapping has syntax errors. \
                    The top level must be a list.')
            if ': ' not in line:
                raise Exception(
                    'The mapping has syntax errors. \
                    Please use ": " as a divider for src and dest.')
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
                    # the commented line would be nicer,
                    # but then you have to keep the next print line,
                    # as the object has to be accessed, otherwise
                    # the object keeps being lazy and __dict__ is not filled
                    # dirty workaround ;-(
                    # print(obj)
                    # self[mappingitem[item]] = eval(selector, obj.__dict__)
                    self[mappingitem[item]] = getattr(obj, selector)

        # postprocess
        for item in codes:
            func = aeval.eval('lambda x, _util: ' +
                              codes[item], globals(), globals())
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

#    @lru_cache(maxsize=None)
    def get(self, item):
        value = self.__getitem__(item)
        if item in self:
            try:
                doc = Node(
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
        docstr = bytes(yaml.dump(native, default_flow_style=False),
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
                if resdoc[query] is False:
                    return False
            if filtertype == 'or':
                if resdoc[query] is True:
                    return True
        if filtertype == 'and':
            return True
        if filtertype == 'or':
            return False

    def preprocess(self, doc, template=None):
        if doc['@type'] == 'zml:image':
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
                args = ['convert', '-resize', size,
                        self.rootdir + '/' + image['url'], thumbfile]
                # add check of return of following line
                subprocess.check_call(args)
                # the following line will set the thumb only in the copy
                # of Node, which will be returned by the listproxy,
                # so changing items of that copy will not affect the
                # original doc (everything before the brackets [] will
                # be untouched. think about it, if its is possible to fix
                # and how to fix that solution would be to use another
                # notation to access the items
                # of a document:
                # doc.get('images',i,'thumb')
                # second solution:
                # dont return Node in the getitem function of Node, but
                # return normal dicts etc. then it will be possible to add
                # a new key to that dict. but: if we dont return Node in the
                # getitem function, we ...
                doc['images'][i]['thumb'] = thumbfile
                o1 = doc['images'][i]
                o2 = doc['images'][i]
        return doc

    def choose_template(self, configtests, filetest,
                        fallback=None, strict=False):
        if configtests is not None and configtests != list() and \
                configtests != [[]]:
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
        doc = self
        filecheck = doc['@type'].replace(':', '_') + '_show'
        if filecheck in dx.config.templates.fe:
            configtest = [dx.config.templates.fe[filecheck]]
        else:
            configtest = None
        filetest = ['fe/' + doc['@type'].replace(':', '_') + '_show' + '.html']
        fallback = 'extensions/base/templates/fe/default_show.html'
        template = self.choose_template(configtest, filetest, fallback)
        doc = self.preprocess(doc, template)
        return doonx.framework.Doonx.render(template, {'c': self.convert(doc)})

    def native(self):
        o = OrderedDict(self)
        for item in o:
            if isinstance(
                o[item],
                Node) or isinstance(
                o[item],
                NodeProxyList) or isinstance(
                o[item],
                    NodeLeafMixin):
                o[item] = o[item].native()
        return o


class UserListSubclass(list):

    def __getslice__(self, i, j):
        return self.__getitem__(slice(i, j))

    def __setslice__(self, i, j, seq):
        return self.__setitem__(slice(i, j), seq)

    def __delslice__(self, i, j):
        return self.__delitem__(slice(i, j))


class NodeProxyList(UserListSubclass):

    def __init__(self, li, db=None, silent=False,
                 root=None, name=None, parent=None):
        # todo: prefill with documents etc during init instead of repeating
        # creating documents after
        self._db = db
        self._root = root
        self._name = name
        self._silent = silent
        self._parent = parent
        for i, item in enumerate(li):
            if isinstance(li[i], dict):
                li[i] = Node(li[i], root=self._root,
                             db=self._db, silent=self._silent)
            elif isinstance(li[i], list):
                li[i] = NodeProxyList(
                    li[i], root=self._root, db=self._db, silent=self._silent)
        super().__init__(li)

    def __setitem__(self, index, value):
        if isinstance(value, dict):
            item = Node(value, root=self._root,
                        db=self._db, silent=self._silent)
        if isinstance(value, list):
            item = NodeProxyList(value, root=self._root,
                                 db=self._db, silent=self._silent)
        if not (isinstance(value, dict) or isinstance(value, list)):
            if len(str(value)) == 32:
                try:
                    item = Node(
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
        # return a new Node each time, which is not what the user expects
        # setting properties and then accessing the object will wipe out
        # the modifications. better convert only during init and setitem
        # and afterwards only return raw items (super.getitem)
        if len(str(r)) == 32:
            try:
                doc = Node(self._db[str(r)], root=self._root,
                           db=self._db, silent=self._silent)
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
            li.append(Node(self._db[str(item)]))
        return li

    def process(self, item):
        if isinstance(item, list) and not isinstance(item, NodeProxyList):
            return NodeProxyList(
                item,
                root=self._root,
                db=self._db,
                silent=self._silent,
                name=self._name)
        if isinstance(item, dict):
            return Node(item, root=self._root,
                        db=self._db, silent=self._silent)

        doc = item
        # if len(str(item))==32:
        #    try:
        #        doc = Node(self._db[str(item)], silent=self.getSilent(), \
        # root=self._root, db=self._db)
        #    except Exception as e:
        #        #debug(e)
        #        doc = item
        return doc

    def __xiter__(self):
        for item in self:
            yield self.process(item)

    def _meta(self, item):
        try:
            if not item.startswith('@'):
                item = '@' + item
            return self._root.get('@type')['@localcontext'][self._name][item]
        except Exception as e:
            debug(e)
            return None

    def native(self):
        l = list(self)
        for i, item in enumerate(l):
            if isinstance(l[i], Node) or isinstance(l[i], NodeLeafMixin):
                l[i] = l[i].native()
        return l


class NodeLeafMixin():

    def __new__(cls, value, name=None, root=None, parent=None):
        return super(NodeLeafMixin, cls).__new__(cls, value)

    def __init__(self, value, name=None, root=None, parent=None):
        super().__init__()
        self._name = name
        self._root = root
        self._parent = parent

    def __call__(self, *args, **kwargs):
        # call f.e. items method of collection
        if self._name in OrderedDict.__dict__:
            return OrderedDict.__dict__[self._name](self._parent)

    def _meta(self, item):
        labels = {
            "_id": "ID",
            "_rev": "Revision",
            "@type": "Type"
        }
        if (item == 'label' or item == '@label') and \
                self._name in labels.keys():
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


class IntLeaf(int, NodeLeafMixin):

    def __new__(cls, value, name=None, root=None, parent=None):
        return super(IntLeaf, cls).__new__(cls, value)

    def __init__(self, value, name=None, root=None, parent=None):
        super().__init__(value, name, root, parent)


class FloatLeaf(float, NodeLeafMixin):

    def __new__(cls, value, name=None, root=None, parent=None):
        return super(FloatLeaf, cls).__new__(cls, value)

    def __init__(self, value, name=None, root=None, parent=None):
        super().__init__(value, name, root, parent)


class StrLeaf(str, NodeLeafMixin):

    def __new__(cls, value, name=None, root=None, parent=None):
        return super(StrLeaf, cls).__new__(cls, value)

    def __init__(self, value, name=None, root=None, parent=None):
        super().__init__(value, name, root, parent)


class BoolLeaf(int, NodeLeafMixin):

    def __new__(cls, value, name=None, root=None, parent=None):
        return super(BoolLeaf, cls).__new__(cls, value)

    def __init__(self, value, name=None, root=None, parent=None):
        super().__init__(value, name, root, parent)

    def __bool__(self):
        if self == 0:
            return False
        else:
            return True


def render(source, localcontext={}, globalcontext=None):
    if source.endswith('.zml'):
        templatefile = source
        l = TemplateLookup(['.'])
        t = l.get_template(templatefile)
        out = t.render(localcontext, globalcontext=globalcontext)
        return out
    else:
        out = Template()._rendercode(source,
                                     localcontext,
                                     globalcontext=globalcontext)
        return out['_root']

zml.debugActive = False


def activateDebug(lfile):
    logging.basicConfig(
        filename=lfile,
        format="%(funcName)s (%(lineno)s) %(message)s",
        level=logging.DEBUG)
    zml.debugActive = True
    logfile = lfile


def debug(out):
    if zml.debugActive:
        logging.debug(out)


class TemplateLookup(object):

    def __init__(self, directories=None,
                 module_directory=None, input_encoding=None):
        self.directories = directories

    def get_template(self, template):
        for d in self.directories:
            abs_path = os.path.join(d, template)
            if os.path.exists(abs_path):
                return Template(abs_path, self)
        return None


def processRoutesSection(lines, i, localcontext, globalcontext):
    route_line_header = indentobj(
        'indent') + '~' + \
        Word(printables, excludeChars=':')('routename') + colon
    res = route_line_header.parseString(lines[i])
    routename = res.routename
    globalcontext['_routes'][res.routename] = dict()
    routesmode_indent_level = len(res.indent)
    remaining_lines = lines[i + 1:]
    l = 0
    for lin in remaining_lines:
        testline = indentobj('indent') + Optional(Word(printables))
        testres = testline.parseString(lin)
        if len(testres.indent) <= routesmode_indent_level:

            return i + l
        else:
            l += 1
        if len(lin) > 0:
            res = route_line.parseString(lin)
        globalcontext['_routes'][routename][res.key] = res.value


def processResourceSection(lines, i, localcontext, globalcontext):

    route_line_header = indentobj('indent') + '&' + \
        Word(printables, excludeChars=':')('resourcename') + \
        colon
    rres = route_line_header.parseString(lines[i])
    datamode_indent_level = len(rres.indent)
    last_indent_level = datamode_indent_level
    globalcontext['_resources'][rres.resourcename] = dict()
    parentnode = globalcontext['_resources']
    current_node_name = rres.resourcename
    data_inline_content = datawords('words')
    dataelement = indentobj('indent') + Optional(name('name')) + \
        id_classes('id_classes')
    dataelement += attributes('attributes') + \
        colon('colon') + Optional(' ')
    dataelement += data_inline_content('inline_content')
    datamode = True
    data_line = indentobj(
        'indent') + Optional(Word(' -$*#<%'))('glyph') + \
        Optional(' ') + dataelement('element')
    res = data_line.parseString(lines[i])
    remaining_lines = lines[i + 1:]
    l = 0
    datablock = ''
    indent_level = datamode_indent_level / 2
    nodestack = list()
    nodestack.append((current_node_name, 0, 'dict'))
    parentstack = list()
    parentstack.append(parentnode)
    current_node_type = 'dict'
    current_list = None
    for lin in remaining_lines:
        res = data_line.parseString(lin)
        relement = res.element
        indent_level = len(res.indent) / 2
        while indent_level <= last_indent_level and last_indent_level > 0:
            if len(nodestack) > 0:
                nodestack.pop(-1)
            if len(nodestack) > 0:
                current_node_name = nodestack[-1][0]
                last_indent_level = nodestack[-1][1]
                current_node_type = nodestack[-1][2]
            if len(parentstack) > 0:
                parentstack.pop(-1)
            if len(parentstack) > 0:
                parentnode = parentstack[-1]
        if indent_level >= last_indent_level:
            if res.glyph.strip() == '-':
                # list node
                if current_node_type == 'list':
                    current_list.append(dict())
                    hanging_list_node = current_list[-1]
                else:
                    current_node_type = 'list'
                    parentnode[current_node_name] = list()
                    parentnode[
                        current_node_name].append(dict())
                    current_list = parentnode[
                        current_node_name]
                    hanging_list_node = parentnode[
                        current_node_name][-1]
                if relement.inline_content != '':
                    parentnode[current_node_name][-1] = relement.inline_content
                else:
                    current_node_name = relement.name
            else:
                # dict node
                if current_node_type == 'list':
                    if relement.inline_content != '':
                        hanging_list_node[
                            relement.name] = relement.inline_content
                    else:
                        if relement.name not in parentnode:
                            parentnode[
                                relement.name] = dict()
                        current_node_name = relement.name
                else:
                    if relement.inline_content != '':
                        if current_node_name not in parentnode:
                            parentnode[current_node_name] = {
                                relement.name: relement.inline_content}
                        else:
                            parentnode[current_node_name][
                                relement.name] = relement.inline_content
                    else:
                        if current_node_name not in parentnode:
                            parentnode[
                                current_node_name] = dict()
                        parentnode = parentnode[
                            current_node_name]
                        current_node_name = relement.name
                    if indent_level > last_indent_level:
                        parentstack.append(parentnode)
                        nodestack.append(
                            (current_node_name,
                             indent_level,
                             current_node_type))
                        last_indent_level = indent_level
        if len(res.indent) <= datamode_indent_level:
            datamode = False
            return i + l
        else:
            datablock += lin
            l += 1


def processDataSection(data_line, lines, i, localcontext, globalcontext):
    res = data_line.parseString(lines[i])
    name = res.element.name
    if 'restdata' in res.element.inline_content:
        localcontext[name] = res.element.inline_content['restdata']
    datamode_indent_level = len(res.indent)
    last_indent_level = datamode_indent_level
    parentnode = localcontext
    current_node_name = res.element.name
    remaining_lines = lines[i + 1:]
    l = 0
    datablock = ''
    indent_level = datamode_indent_level / 2
    nodestack = list()
    nodestack.append((current_node_name, 0, 'dict'))
    parentstack = list()
    parentstack.append(parentnode)
    current_node_type = 'dict'
    current_list = None
    for lin in remaining_lines:
        res = data_line.parseString(lin)
        relement = res.element
        indent_level = len(res.indent) / 2
        while indent_level <= last_indent_level and last_indent_level > 0:
            if len(nodestack) > 0:
                nodestack.pop(-1)
            if len(nodestack) > 0:
                current_node_name = nodestack[-1][0]
                last_indent_level = nodestack[-1][1]
                current_node_type = nodestack[-1][2]
            if len(parentstack) > 0:
                parentstack.pop(-1)
            if len(parentstack) > 0:
                parentnode = parentstack[-1]
        if indent_level >= last_indent_level:
            if res.glyph.strip() == '-':
                # list node
                if current_node_type == 'list':
                    current_list.append(dict())
                    hanging_list_node = current_list[-1]
                else:
                    current_node_type = 'list'
                    parentnode[current_node_name] = list()
                    parentnode[
                        current_node_name].append(dict())
                    current_list = parentnode[
                        current_node_name]
                    hanging_list_node = parentnode[
                        current_node_name][-1]
                if relement.inline_content != '':
                    parentnode[current_node_name][-1] = relement.inline_content
                else:
                    current_node_name = relement.name
            else:
                # dict node
                if current_node_type == 'list':
                    if relement.inline_content != '':
                        hanging_list_node[
                            relement.name] = relement.inline_content
                    else:
                        if relement.name not in parentnode:
                            parentnode[
                                relement.name] = dict()
                        current_node_name = relement.name
                else:
                    if relement.inline_content != '':
                        if current_node_name not in parentnode:
                            parentnode[current_node_name] = {
                                relement.name: relement.inline_content}
                        else:
                            parentnode[current_node_name][relement.name] = \
                                relement.inline_content
                    else:
                        if current_node_name not in parentnode:
                            parentnode[
                                current_node_name] = dict()
                        parentnode = parentnode[
                            current_node_name]
                        current_node_name = relement.name
                    if indent_level > last_indent_level:
                        parentstack.append(parentnode)
                        nodestack.append(
                            (current_node_name,
                             indent_level,
                             current_node_type))
                        last_indent_level = indent_level
        if len(res.indent) <= datamode_indent_level:
            datamode = False
            return i + l
        else:
            datablock += lin
            l += 1


class Template(object):

    def __init__(self, template=None, lookup=None, viewhelperdir=None):
        self.template = template
        self.lookup = lookup
        self.viewhelperdir = viewhelperdir
        self.localcontext = dict()
        self.globalcontext = dict()
        self.globalcontext['_routes'] = dict()
        self.globalcontext['_resources'] = dict()
        self.namespacemode = False
        self.namespaces = dict()

    def getResourcePath(self, t=None):
        restdata = None
        if 'resourcename' in t:
            host = self.globalcontext['_resources'][t.resourcename]['host']
            if 'port' in self.globalcontext['_resources'][t.resourcename]:
                port = self.globalcontext['_resources'][t.resourcename]['port']
            else:
                port = 80
            username = None
            password = None
            if 'username' in self.globalcontext['_resources'][t.resourcename]:
                username = self.globalcontext['_resources'][
                    t.resourcename]['username']
            if 'password' in self.globalcontext['_resources'][t.resourcename]:
                password = self.globalcontext['_resources'][
                    t.resourcename]['password']
            hostport = "%s:%s" % (host, port)
            r = zml.rest.Resource(hostport, username, password)
            restdata = r.get(t.path)
            return {'restdata': restdata}
        else:
            return {}

    def render(
            self,
            localcontext=None,
            template=None,
            importmode=False,
            globalcontext=None):
        self.localcontext.update(localcontext)
        if globalcontext is not None:
            self.globalcontext = globalcontext
        out = self._render(localcontext, template, importmode=importmode)
        return out['_root']

    def intercode_line(
            self,
            code_indent_level,
            localcontext_item,
            foo,
            comment=''):
        res = ' ' * 2 * code_indent_level
        res += "write('%s', '%s\\n') %s \n" % (
            localcontext_item, foo, comment)
        return res

    def _render(self, localcontext=None, template=None, indent_global='',
                importmode=False):
        self.localcontext.update(localcontext)
        if template is None:
            templatepath = self.template
        else:
            if self.lookup is None:
                templatepath = template
            else:
                templateobj = self.lookup.get_template(template)
                templatepath = templateobj.template
        with open(templatepath, 'r', encoding='utf-8') as f:
            zmlcode = f.read()
        return self._rendercode(zmlcode, localcontext, importmode=importmode)

    def _rendercode(
            self,
            zmlcode=None,
            localcontext=None,
            indent_global='',
            importmode=False,
            code_indent_level=0,
            localcontext_item='_root',
            globalcontext=None):
        self.localcontext.update(localcontext)
        if globalcontext is not None:
            self.globalcontext = globalcontext
        code_indent_last = code_indent_level * 2
        datamode = False
        datamode_indent_level = 0

        def escape_word(*args, **kwargs):
            return html.escape(args[2][0])
        code_indents = list()
        indents = list()
        lines = zmlcode.split('\n')[:-1]
        output = ''
        indent_last = ''
        tag_last = ''
        indents = list()
        code_indents = list()
        last_was_inline = False
        inherit_file = None
        lrev = list(reversed(lines))
        last_line = 0

        for i, line in enumerate(lrev):
            if len(line) == 0:
                last_line = len(lines) - i - 1
                continue
            else:
                break
        lastnewline = False
        cil = ''
        inherit_file = None
        explicit_mode = False
        code_block_active = False

        lnum = 0
        self.jump_to = 0
        last_was_text = False
        # check indentation, should be a multiple of 2
        for i, line in enumerate(lines):
            err = 'Indentation on line %s is not a multiple of 2' % i
            linecheck = indentobj('indent') + Word(printables)
            if len(line.strip()) > 0:
                check = linecheck.parseString(line)
                if not len(check.indent) % 2 == 0:
                    return {
                        '_root': err}
        for i, line in enumerate(lines):
            is_text = False
            indstrs = [ind[0] for ind in indents]
            indstr = ','.join(indstrs)
            if self.jump_to > 0:
                if i < self.jump_to + 1:
                    continue
                else:
                    self.jump_to = 0
            code_indent_level = int(code_indent_last / 2)
            newline = False
            if len(line.strip()) == 0:
                newline = True
            if line.strip().startswith('"'):
                res = explicit_single_line.parseString(line)
                ic = res.inline_content.replace("'''", "")
                ic = "'+%s+'" % (ic)
                output += self.intercode_line(
                    code_indent_level, localcontext_item,
                    indent_global + res.indent + ic)
                last_was_inline = False
                continue
            if line.strip().startswith("'''") and \
               line.strip().endswith("'''") and \
               len(line.strip()) > 3:
                res = explicit_line.parseString(line.replace("'''", ""))
                ic = res.inline_content.replace("'''", "")
                ic = "'+%s+'" % (ic)
                output += self.intercode_line(
                    code_indent_level, localcontext_item,
                    indent_global + res.indent + ic)
                last_was_inline = False
                continue
            if line.strip() == "'''":
                debug('explicit_mode')
                debug(line)
                explicit_mode = not explicit_mode
                continue
            indent_reduction = False
            if code_block_active:
                if line.strip().endswith('%>'):
                    code_block_active = False
                    if line.strip().startswith('<%'):
                        res = code_inlineblock.parseString(line)
                        output += res.code[0]
                else:
                    output += line + '\n'
            else:
                output += "# line: %s \n" % (line)
                if line.strip().startswith('#'):
                    if line.strip('#').strip().startswith('inherit'):
                        res = inherit_line.parseString(line)
                        inherit_file = res.templatefile
                    if line.strip('#').strip().startswith('namespace'):
                        res = namespace_line.parseString(line)
                        nsid = res.nsid
                        namespace = res.namespace
                        self.localcontext['_namespace'] = nsid
                        self.namespacemode = True
                    if line.strip('#').strip().startswith('import'):
                        debug(line)
                        res = import_line.parseString(line)
                        m = res.module
                        (ns, components) = self.parseComponents(res.module)
                        self.namespaces[ns] = components
                elif line.strip().startswith('*'):
                    localcontext_item = line[1:-1]
                    self.localcontext[localcontext_item] = ''
                elif line.strip().startswith('~'):
                    self.jump_to = processRoutesSection(
                        lines, i, self.localcontext, self.globalcontext)
                elif line.strip().startswith('&'):
                    self.jump_to = processResourceSection(
                        lines, i, self.localcontext, self.globalcontext)
                elif line.strip().startswith('$'):
                    resourcepath = '@' + \
                        Word(printables,
                             excludeChars=': @ /')('resourcename') + \
                        Word(printables)('path')
                    resourcepath.setParseAction(self.getResourcePath)
                    data_inline_content = resourcepath(
                        'resourcepath') | datawords('words')
                    dataelement = indentobj('indent') + \
                        Optional(name('name')) + \
                        id_classes('id_classes')
                    dataelement += attributes('attributes') + \
                        colon('colon') + Optional(' ')
                    dataelement += data_inline_content('inline_content')
                    datamode = True
                    data_line = indentobj(
                        'indent') + Optional(Word(' -$*#<%'))('glyph') + \
                        Optional(' ') + dataelement('element')
                    self.jump_to = processDataSection(
                        data_line, lines, i,
                        self.localcontext, self.globalcontext)
                    c = Node(self.localcontext)
                    globals().update(c)
                elif line.strip().startswith('%'):
                    res = code_inline.parseString(line)
                    debug('code line')
                    code = " ".join(res.code)
                    output += "# code line \n"
                    output += "# len code indents: %s \n" % len(code_indents)
                    if len(code_indents) > 0:
                        code_indents_greater = [
                            ind for ind in code_indents
                            if len(ind[1]) >= len(res.indent)]
                        if len(code_indents_greater) > 0:
                            code_indents_greater.reverse()
                        for ind in code_indents_greater:
                            code_indents.pop(-1)
                            tag = ind[0]
                            if len(res.indent) <= len(ind[1]):
                                code_indent_level -= 1
                    code_indents.append([code, res.indent])
                    if code_indent_level < 0:
                        code_indent_level = 0
                    if len(res.indent) <= code_indent_last and \
                       len(code_indents) > 0:
                        code_indents_greater = [
                            ind for ind in code_indents
                            if len(ind[1]) >= len(res.indent)]
                        if len(code_indents_greater) > 0:
                            code_indents_greater.reverse()
                        for ind in code_indents_greater:
                            code_indents.pop(-1)
                            tag = ind[0]
                    if code_indent_level < 0:
                        code_indent_level = 0
                    if len(res.indent) <= len(indent_last) and \
                       len(indents) > 0:
                        indents_greater = [
                            ind for ind in indents
                            if len(ind[1]) >= len(res.indent)]
                        if len(indents_greater) > 0:
                            indents_greater.reverse()
                        for ind in indents_greater:
                            indents.pop(-1)
                            tag = ind[0]
                            indx = ind[1]
                            cindent = ind[2]
                            if last_was_inline:
                                indent_visible = ""
                                last_was_inline = False
                            else:
                                indent_visible = indx
                            output += "# tag: %s\n" % tag
                            output += self.intercode_line(
                                cindent, localcontext_item, indent_global +
                                indent_visible + "</%s>" % tag)
                    # end close pending tags
                    output += "# code_indent_level: %s \n" % code_indent_level
                    output += ' ' * 2 * code_indent_level + code.strip() + '\n'
                    if code.strip().endswith(':'):
                        code_indent_level += 1
                elif line.strip().startswith('<%'):
                    code_block_active = True
                    if line.strip().endswith('%>'):
                        res = code_inlineblock.parseString(line)
                        output += res.code[0]
                        code_block_active = False
                elif line.strip().startswith('{'):
                    res = moustache_line.parseString(line)
                    if res.expression in self.localcontext:
                        c = self.localcontext[res.expression].split('\n')[:-1]
                        for lin in c:
                            output += ' ' * 2 * code_indent_level + \
                                "write('%s', '%s\\n')\n" % (
                                    localcontext_item,
                                    indent_global +
                                    res.indent[(code_indent_level + 1) * 2:] +
                                    lin)
                    else:
                        try:
                            output += ' ' * 2 * code_indent_level + \
                                "write('" + localcontext_item + "', " + \
                                indent_global + \
                                res.indent[code_indent_level * 2:] + \
                                "str(" + res.expression + ")+'\\n')\n"
                        except Exception as e:
                            debug(e)
                elif len(line.strip()) == 0:
                    newline = True
                elif explicit_mode:
                    debug('explicit mode')
                    res = explicit_line.parseString(line)
                    ic = res.inline_content.replace("'''", "")
                    ic = "'+" + ic + "+'"
                    output += self.intercode_line(
                        code_indent_level, localcontext_item,
                        indent_global + res.indent + ic)
                    last_was_inline = False
                elif not hasInlineColon.parseString(line).has_colon:
                    debug('no colon')
                    res = element_empty.parseString(line)
                    if '-' in res.name:
                        indentedrawcode = ''
                        unindentedrawcode = ''
                        resx = viewhelper.parseString(line)
                        _params = dict()
                        for item in resx.attribs:
                            # _params[item.key] = item.value
                            snipcode = item.key + '=' + item.value
                            indentedrawcode += ' ' * 2 * code_indent_level + \
                                snipcode + '\n'
                            unindentedrawcode += snipcode + '\n'
                        params = '_params={'
                        flatparams = [
                            "'%s':%s" %
                            (j, k) for j, k in _params.items()]
                        flatparamstr = ', '.join(flatparams)
                        params += flatparamstr + '}'
                        snipcode += params
                        indentedrawcode += ' ' * 2 * code_indent_level + \
                            params + '\n'
                        unindentedrawcode += params + '\n'
                        code_globals = globals()
                        code_locals = locals()
                        output += indentedrawcode
                        attr = res.attributes
                        c = dict()
                        ns = res.name.split('-')[0]
                        viewhelperlocalcontext = {}
                        cc = self.namespaces[resx.namespace][resx.name]
                        componentcode = cc
                        compo = ''
                        for l in componentcode.split('\n'):
                            compo += ' ' * 2 * code_indent_level + l + '\n'
                        cr = self._rendercode(
                            compo,
                            _params,
                            importmode=True,
                            code_indent_level=code_indent_level,
                            localcontext_item=localcontext_item)
                        componentres = cr
                        output += componentres
                    else:
                        if len(res.indent) == 0:
                            localcontext_item = '_root'
                            res.indent = ''
                        if len(code_indents) > 0:
                            code_indents_greater = [
                                ind for ind in code_indents
                                if len(ind[1]) >= len(res.indent)]
                            if len(code_indents_greater) > 0:
                                code_indents_greater.reverse()
                            for ind in code_indents_greater:
                                code_indents.pop(-1)
                                tag = ind[0]
                                if len(res.indent) < len(ind[1]):
                                    code_indent_level -= 1
                        if code_indent_level < 0:
                            code_indent_level = 0
                        if len(res.indent) <= len(indent_last) and \
                           len(indents) > 0:
                            indents_greater = [
                                ind for ind in indents
                                if len(ind[1]) >= len(res.indent)]
                            if len(indents_greater) > 0:
                                indents_greater.reverse()
                            for ind in indents_greater:
                                indents.pop(-1)
                                tag = ind[0]
                                cindent = ind[2]
                                code_indent_level = ind[2]
                                if last_was_inline:
                                    indent_visible = ""
                                    last_was_inline = False
                                else:
                                    indent_visible = ind[1]
                                output += self.intercode_line(
                                    cindent, localcontext_item, indent_global +
                                    indent_visible + "</%s>" % tag)
                                if code_indent_level < 0:
                                    code_indent_level = 0
                        void_elements = [
                            'area', 'base', 'br', 'col', 'command',
                            'embed', 'hr', 'img', 'input', 'keygen',
                            'link', 'meta', 'param', 'source', 'track', 'wbr']
                        if res.name in void_elements:
                            closing_tag = ''
                        else:
                            closing_tag = '</%s>' % res.name
                        output += self.intercode_line(
                            code_indent_level, localcontext_item,
                            indent_global +
                            res.indent[code_indent_level * 2:] + "<%s%s %s>" %
                            (res.name, res.id_classes, res.attributes) +
                            closing_tag)
                elif checkComponent(line):
                    indent_line = indentobj('indent') + Optional(name('name'))
                    res = indent_line.parseString(line)
                    # close greater indents before processing further
                    if len(res.indent) <= len(indent_last) and \
                       len(indents) > 0:
                        indents_greater = [
                            ind for ind in indents
                            if len(ind[1]) >= len(res.indent)]
                        if len(indents_greater) > 0:
                            indents_greater.reverse()
                        for ind in indents_greater:
                            allind = ind[1]
                            indents.pop(-1)
                            tag = ind[0]
                            cindent = ind[2]
                            output += "# d4 %s\n" % tag
                            if last_was_inline:
                                indent_visible = ""
                                last_was_inline = False
                            else:
                                indent_visible = ind[1]
                            output += self.intercode_line(
                                cindent, localcontext_item, indent_global +
                                indent_visible + "</%s>" % tag, '# d2')
                            cil = cindent
                            code_indent_level = cil

                    remaining_lines = lines[i + 1:]
                    component_indent = res.indent
                    childs = list()
                    n = 0
                    childs.append('')
                    l = 0
                    for lin in remaining_lines:
                        r = indent_line.parseString(lin)
                        indentlen = len(r.indent)
                        if indentlen <= len(res.indent):
                            break
                        if l > 0 and indentlen == len(res.indent) + 2:
                            childs.append('')
                            n += 1
                        childs[n] += lin + '\n'
                        l += 1
                    if l > 0:
                        self.jump_to = i + l
                    childitems = list()
                    for childcode in childs:
                        if len(childcode) > 0:
                            childres = render(childcode, localcontext)
                            childitems.append(childres)
                    ic = element.parseString(line).inline_content
                    if len(ic) > 0:
                        childitems.append(ic.strip("'"))
                    indentedrawcode = ''
                    unindentedrawcode = ''
                    resx = viewhelper.parseString(line)
                    _params = dict()
                    snipcode = ''
                    for item in resx.attribs:
                        _params[item.key] = item.value
                        # snipcode = item.key + '=' + item.value
                        # indentedrawcode += ' ' * 2 * code_indent_level + \
                        #    snipcode + '\n'
                        # unindentedrawcode += snipcode + '\n'
                    params = '_params={'
                    flatparams = [
                        "'%s':%s" %
                        (j, k) for j, k in _params.items()]
                    flatparamstr = ', '.join(flatparams)
                    params += flatparamstr + '}'
                    snipcode += params
                    code_globals = globals()
                    code_locals = locals()
                    output += indentedrawcode
                    attr = res.attributes
                    c = dict()
                    ns = res.name.split('-')[0]
                    viewhelperlocalcontext = {}
                    cc = self.namespaces[resx.namespace][resx.name]
                    componentcode = cc
                    compo = ''
                    # compo += unindentedrawcode
                    for l in componentcode.split('\n'):
                        compo += ' ' * 2 * code_indent_level + l + '\n'
#                   _childs localcontext item is deprecated and
#                   will be removed in the next release
                    componentcontext = dict()
                    componentcontext.update({
                        '_children': childitems,
                        '_childs': childitems})
                    componentcontext.update(_params)
                    componentcontext['_params'] = _params
#                    cr = self._rendercode(
#                            compo,
#                            _params,
#                            importmode=True,
#                            code_indent_level=code_indent_level,
#                            localcontext_item=localcontext_item)
#                    output += 'write("""' + localcontext_item + \
#                        '""" , """ ' + componentres + '""")'
                    cr = render(
                        compo,
                        componentcontext,
                        globalcontext=self.globalcontext)
                    componentres = cr
                    output += 'write("""' + localcontext_item + \
                        '""" , """ ' + componentres + '""")'
                elif hasInlineColon.parseString(line).has_colon:
                    debug('colon')
                    debug(line)
                    res = element.parseString(line)
                    if len(res.name) == 0:
                        is_text = True
                    cil = 0
                    rawline = line.strip()
                    allindent = len(res.indent)
                    codeindent = code_indent_last
                    contentindent = allindent - codeindent
                    if len(res.indent) == 0:
                        localcontext_item = '_root'
                        res.indent = ''
                    code_indent_level_tmp = code_indent_level
                    # reduce code_indent_level
                    if len(code_indents) > 0:
                        code_indents_greater = [
                            ind for ind in code_indents
                            if len(ind[1]) >= len(res.indent)]
                        if len(code_indents_greater) > 0:
                            code_indents_greater.reverse()
                        for ind in code_indents_greater:
                            code_indents.pop(-1)
                            tag = ind[0]
                            if len(res.indent) <= len(ind[1]):
                                code_indent_level -= 1
                                cil = code_indent_level
                    if code_indent_level < 0:
                        code_indent_level = 0
                    if len(res.indent) <= len(indent_last) and \
                       len(indents) > 0:
                        indents_greater = [
                            ind for ind in indents
                            if len(ind[1]) >= len(res.indent)]
                        if len(indents_greater) > 0:
                            indents_greater.reverse()
                        for ind in indents_greater:
                            allind = ind[1]
                            indents.pop(-1)
                            tag = ind[0]
                            cindent = ind[2]
                            output += "# d3 %s\n" % tag
                            if last_was_inline:
                                indent_visible = ""
                                last_was_inline = False
                            else:
                                indent_visible = ind[1]
                            output += self.intercode_line(
                                cindent, localcontext_item, indent_global +
                                indent_visible + "</%s>" % tag, '# d2')
                            cil = cindent
                            code_indent_level = min(code_indent_level, cil)
                    if len(res.name) > 0:
                        indents.append([
                            res.name,
                            res.indent,
                            code_indent_level])
                    ic = res.inline_content.replace("'''", "")
                    if lastnewline:
                        if cil < code_indent_last:
                            output += ' ' * 2 * cil + \
                                "write('%s', '%s\\n') # last nl1\n" % (
                                    localcontext_item, indent_global +
                                    res.indent[(code_indent_level + 1) * 2:])
                        else:
                            output += ' ' * code_indent_last + \
                                "write('%s', '%s\\n') # last nl2\n" % (
                                    localcontext_item, indent_global +
                                    res.indent[(code_indent_level + 1) * 2:])
                    if ic is None or ic == '':
                        ic = "''"
                    spacer = ''
                    if len(res.attributes) > 0:
                        spacer = ' '
                    if lastnewline and cil < code_indent_level:
                        if len(res.name) > 0:
                            output += ' ' * 2 * cil + \
                                "write('" + localcontext_item + \
                                "', '%s%s<%s%s%s%s>'+%s) # d1a\n" % (
                                    indent_global,
                                    res.indent[code_indent_level * 2:],
                                    res.name, res.id_classes, spacer,
                                    res.attributes, ic)
                        else:
                            output += ' ' * 2 * cil + \
                                "write('" + localcontext_item + \
                                "', '%s%s'+%s) # d1a\n" % (
                                    indent_global,
                                    res.indent[code_indent_level * 2:],
                                    ic)
                        if res.inline_content == '':
                            output += ' ' * 2 * cil + \
                                "write('" + localcontext_item + \
                                "', '\\n')\n"
                    else:
                        if res.name == 'html':
                            output += "write('" + localcontext_item + \
                                "', '<!DOCTYPE html>\\n')\n"
                        if len(res.name) > 0:
                            if last_was_text:
                                indent_vis = ''
                            else:
                                indent_vis = res.indent[code_indent_level * 2:]
                            output += ' ' * 2 * code_indent_level + \
                                "write('" + localcontext_item + \
                                "', '%s%s<%s%s%s%s>'+%s) # d1b1\n" % (
                                    indent_global,
                                    indent_vis,
                                    res.name, res.id_classes, spacer,
                                    res.attributes, ic)
                        else:
                            if last_was_text:
                                indent_vis = ''
                            else:
                                indent_vis = res.indent[code_indent_level * 2:]
                            output += ' ' * 2 * code_indent_level + \
                                "write('" + localcontext_item + \
                                "', '%s%s'+%s+'\\n') # d1b2\n" % (
                                    indent_global,
                                    indent_vis,
                                    ic)
                        if res.inline_content == '':
                            output += ' ' * 2 * code_indent_level + \
                                "write('" + localcontext_item + "', '\\n')\n"
                    if len(res.inline_content) > 0:
                        last_was_inline = True
                    else:
                        last_was_inline = False
                    indent_last = res.indent
                    tag_last = res.name
                if "'''" in line:
                    explicit_mode = not explicit_mode
                last_was_text = is_text
            if lastnewline:
                lastnewline = False
            lastnewline = newline
            if lastnewline:
                last_indent_level = 0
                code_indent_last = 0
                cil = 0
            code_indent_last = code_indent_level * 2
            cil = code_indent_last
            for indent in indents:
                output += "# tag: %s indent: %s \n" % (
                    indent[0], len(indent[1]))
            lnum += 1

        if len(indents) > 0:
            indents.reverse()
        for ind in indents:
            tag = ind[0]
            if last_was_inline:
                indent_visible = ''
                last_was_inline = False
            else:
                indent_visible = ind[1]
            output += ' ' * 2 * ind[2] + \
                "write('" + localcontext_item + "', '%s</%s>\\n')\n" % (
                    (indent_global + indent_visible)[ind[2] * 2:], tag)
            if len(ind[1]) <= code_indent_last:
                code_indent_level -= 1
                code_indent_last = code_indent_level
        localcontext = Node(self.localcontext)
        # localcontext = self.localcontext
        debug(output)
        if importmode:
            return output
        else:
            localcontext['write'] = self.write
            localcontext['_path'] = self._path
            globals().update(localcontext)
            saeval = Interpreter(localcontext)
            saeval.eval(output)

        if inherit_file is not None:
            self.localcontext = self._render(self.localcontext, inherit_file)
        return self.localcontext

    def set_templatedir(self, templatedir):
        self.templatedir = templatedir

    def set_viewhelperdir(self, viewhelperdir):
        self.viewhelperdir = viewhelperdir

    def write(self, localcontext_item, code):
        if localcontext_item not in self.localcontext:
            self.localcontext[localcontext_item] = ''
        self.localcontext[localcontext_item] += code

    def parseComponents(self, template):
        namespace_line = Suppress('#') + Suppress('namespace') + \
            Word(printables, excludeChars="=")('nsid')
        namespace_line += '=' + Word(printables)('namespace')
        if template is None:
            templatepath = self.template
        else:
            if self.lookup is None:
                templatepath = template
            else:
                templateobj = self.lookup.get_template(template)
                templatepath = templateobj.template
        with open(templatepath, 'r', encoding='utf-8') as f:
            zmlcode = f.read()
            lines = zmlcode.split('\n')[:-1]
        components = dict()
        componentname = '_root'
        components[componentname] = list()
        namespace = '_default'
        for i, line in enumerate(lines):
            if line.strip().startswith('#'):
                if line.strip('#').strip().startswith('namespace'):
                    res = namespace_line.parseString(line)
                    nsid = res.nsid
                    namespace = res.nsid
            if line.startswith('*') and line.endswith(':'):
                componentname = line[1:-1]
                components[componentname] = list()
            else:
                # components[componentname].append(line[2:])
                components[componentname].append(line[:])
        for component in components:
            components[component] = '\n'.join(components[component])
        return namespace, components

    def _path(self, action, params):
        if action.startswith("'") and action.endswith("'"):
            action = action[1:-1]
        pathbase = self.globalcontext['_routes']['routes'][action]
        routemoustache = Suppress('{') + \
            Word(printables, excludeChars="{}'")('routevar') + \
            Suppress('}')
        routeline = routemoustache | Word(
            printables, excludeChars="{}'")('pathsegment')
        # routeline.setParseAction(self.renderRouteItems)
        routeitems = pathbase.split('/')
        path = list()
        for routeitem in routeitems:
            if routeitem != '':
                res = routeline.parseString(routeitem)
                if res.pathsegment:
                    path.append(res.pathsegment)
                if res.routevar:
                    if res.routevar in globals():
                        path.append(globals()[res.routevar].replace("'", ''))
                    else:
                        return 'Missing route variable %s' % res.routevar
        return '/' + '/'.join(path)
