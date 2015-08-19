import json
from urllib.parse import urljoin

from zope.component import getMultiAdapter
from zope.schema import getFieldsInOrder

from bst.pygasus.core import ext
from bst.pygasus.scaffolding import interfaces
from bst.pygasus.wsgi.interfaces import IRequest
from bst.pygasus.core.interfaces import IBaseUrl
from bst.pygasus.core.interfaces import IApplicationContext
from bst.pygasus.scaffolding import loader
from builtins import super

from genshi.template import NewTextTemplate

# !!! for this module we use OrderedDict as dict !!!
from collections import OrderedDict as dict

CLASS_NAMESPACE = 'scaffolding'
EXT_DEFINE_CLASS = 'Ext.define("%s", %s);'


class BaseRecipe(ext.MultiAdapter):
    ext.baseclass()
    ext.adapts()

    def __init__(self, context, descriptive, request):
        self.context = context
        self.descriptive = descriptive
        self.request = request

    def buildclass(self, name, extclass):
        return EXT_DEFINE_CLASS % (name, json.dumps(extclass, indent=' ' * 4),)

    def classname(self, namespace, type, name):
        return '%s.%s.%s' % (namespace, type, name)

    def render_template(self, tpl_name):
        tmpl = loader.load(tpl_name, cls=NewTextTemplate)
        stream = tmpl.generate(view=self)
        return stream.render()


@ext.implementer(interfaces.IScaffoldingRecipeModel)
class Model(BaseRecipe):
    ext.name('model')
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive, IRequest)

    def __call__(self):
        fields = list()
        for name, zfield in getFieldsInOrder(self.descriptive.interface):
            fields.append(getMultiAdapter((self, zfield,), interfaces.IFieldBuilder)())
        model = dict(extend='Ext.data.Model',
                     fields=fields)
        classname = self.classname(CLASS_NAMESPACE, 'model', self.descriptive.classname)
        return self.buildclass(classname, model)


class BaseStore(BaseRecipe):
    ext.baseclass()
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive, IRequest)

    def __init__(self, context, descriptive, request):
        super(BaseStore, self).__init__(context, descriptive, request)

    def __call__(self):
        return self.render_template('store.json.tpl')

    @property
    def url(self):
        return IBaseUrl(self.request).url('data/%s' % self.descriptive.classname)

    @property
    def name(self):
        return self.descriptive.classname

    @property
    def cname(self):
        return self.classname(CLASS_NAMESPACE, 'store', self.descriptive.classname)

    @property
    def model(self):
        return self.classname(CLASS_NAMESPACE, 'model', self.descriptive.classname)

    @property
    def buffered(self):
        return False

    @property
    def autoSync(self):
        return True


@ext.implementer(interfaces.IScaffoldingRecipeStore)
class Store(BaseStore):
    ext.name('store')
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive, IRequest)


@ext.implementer(interfaces.IScaffoldingRecipeBufferedStore)
class BufferedStore(BaseStore):
    ext.name('bufferedstore')
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive, IRequest)

    def __call__(self):
        return self.render_template('store.json.tpl')

    @property
    def name(self):
        return 'Buffered%s' % self.descriptive.classname

    @property
    def cname(self):
        return self.classname(CLASS_NAMESPACE, 'bufferedstore', self.descriptive.classname)

    @property
    def buffered(self):
        return True

    @property
    def autoSync(self):
        return False


class BaseForm(BaseRecipe):
    ext.baseclass()
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive, IRequest)

    aliasprefix = 'Form'

    def __call__(self):
        return self.render_template('form.json.tpl')

    @property
    def title(self):
        return self.descriptive.title

    @property
    def items(self):
        items = list()
        for name, zfield in getFieldsInOrder(self.descriptive.interface):
            items.append(getMultiAdapter((self, zfield,), interfaces.IFieldBuilder)())
        return items

    @property
    def name(self):
        return self.classname(CLASS_NAMESPACE, self.aliasprefix.lower(), self.descriptive.classname)


@ext.implementer(interfaces.IScaffoldingRecipeForm)
class Form(BaseForm):
    ext.name('form')
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive, IRequest)


@ext.implementer(interfaces.IScaffoldingRecipeDisplay)
class Display(BaseForm):
    ext.name('display')
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive, IRequest)

    aliasprefix = 'Display'


@ext.implementer(interfaces.IScaffoldingRecipeGrid)
class Grid(BaseRecipe):
    ext.name('grid')
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive, IRequest)

    def __call__(self):
        return self.render_template('grid.json.tpl')

    @property
    def title(self):
        return self.descriptive.title

    @property
    def name(self):
        return self.classname(CLASS_NAMESPACE, 'grid', self.descriptive.classname)

    @property
    def columns(self):
        columns = list()
        for name, zfield in getFieldsInOrder(self.descriptive.interface):
            columns.append(getMultiAdapter((self, zfield,), interfaces.IFieldBuilder)())
        return columns

    @property
    def alias(self):
        return 'widget.Grid%s' % self.descriptive.classname

    @property
    def requires(self):
        return self.classname(CLASS_NAMESPACE, 'bufferedstore', self.descriptive.classname)

    @property
    def store(self):
        name = self.classname(CLASS_NAMESPACE, 'bufferedstore', self.descriptive.classname)
        return 'Ext.create("%s")' % name


@ext.implementer(interfaces.IScaffoldingRecipeEditGrid)
class EditGrid(Grid):
    ext.name('editgrid')
    ext.provides(interfaces.IScaffoldingRecipeEditGrid)
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive, IRequest)

    def __call__(self):
        return self.render_template('editgrid.json.tpl')

    @property
    def alias(self):
        return 'widget.EditGrid%s' % self.descriptive.classname

    @property
    def name(self):
        return self.classname(CLASS_NAMESPACE, 'editgrid', self.descriptive.classname)
