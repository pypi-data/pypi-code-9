import json
from zope import schema
from zope.i18n import translate
from zope.schema.vocabulary import getVocabularyRegistry

from bst.pygasus.core import ext
from bst.pygasus.scaffolding import loader
from bst.pygasus.scaffolding.fields import BuilderBase
from bst.pygasus.scaffolding.interfaces import IScaffoldingRecipeGrid

from genshi.template import NewTextTemplate


class DefaultField(BuilderBase):
    ext.adapts(IScaffoldingRecipeGrid, schema.interfaces.IField)

    def __call__(self):
        di = dict(dataIndex=self.field.getName(),
                  text=translate(self.field.title,
                                 context=self.recipe.request)
                  )
        return json.dumps(di, indent=' ' * 4)


class DateField(DefaultField):
    ext.adapts(IScaffoldingRecipeGrid, schema.interfaces.IDate)

    def __call__(self):
        di = json.loads(super(DateField, self).__call__())
        di.update(dict(xtype='datecolumn',
                       dateFormat='Y-m-d H:i:s.u'))
        return json.dumps(di, indent=' ' * 4)


class TimeField(DefaultField):
    ext.adapts(IScaffoldingRecipeGrid, schema.interfaces.ITime)

    def __call__(self):
        di = json.loads(super(DateField, self).__call__())
        di.update(dict(xtype='timecolumn',
                       dateFormat='H:i:s.u'))
        return json.dumps(di, indent=' ' * 4)


class FloatField(DefaultField):
    ext.adapts(IScaffoldingRecipeGrid, schema.interfaces.IFloat)

    def __call__(self):
        di = json.loads(super(FloatField, self).__call__())
        di.update(dict(xtype='numbercolumn'))
        return json.dumps(di, indent=' ' * 4)


class ChoiceField(DefaultField):
    ext.adapts(IScaffoldingRecipeGrid, schema.interfaces.IChoice)

    def __call__(self):
        di = json.loads(super(ChoiceField, self).__call__())
        di['renderer'] = '%renderer%'
        di = json.dumps(di, indent=' ' * 4)

        # Render the template
        tmpl = loader.load('combobox_renderer.json.tpl', cls=NewTextTemplate)
        stream = tmpl.generate(view=self)
        di = di.replace('"%renderer%"', stream.render())
        return di

    @property
    def terms(self):
        vr = getVocabularyRegistry()
        return vr.get(None, self.field.vocabularyName)
