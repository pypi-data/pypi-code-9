import json

from zope import schema
from zope.i18n import translate
from zope.schema.vocabulary import getVocabularyRegistry

from bst.pygasus.core import ext
from bst.pygasus.scaffolding import loader
from bst.pygasus.scaffolding.fields import BuilderBase
from bst.pygasus.scaffolding.fields import column
from bst.pygasus.scaffolding.fields import form
from bst.pygasus.scaffolding.interfaces import IScaffoldingRecipeEditGrid

from genshi.template import NewTextTemplate

class DefaultField(BuilderBase):
    ext.adapts(IScaffoldingRecipeEditGrid, schema.interfaces.IField)

    def __call__(self):
        di = dict(dataIndex=self.field.getName(),
                  text=translate(self.field.title,
                                 context=self.recipe.request),
                  field=dict(xtype='textfield'))
        return json.dumps(di, indent=' ' * 4)


class PasswordField(DefaultField):
    ext.adapts(IScaffoldingRecipeEditGrid, schema.interfaces.IPassword)

    def __call__(self):
        di = json.loads(super(PasswordField, self).__call__())
        di.update(dict(inputType='password'))
        return json.dumps(di, indent=' ' * 4)


class DateField(DefaultField):
    ext.adapts(IScaffoldingRecipeEditGrid, schema.interfaces.IDate)

    def __call__(self):
        di = json.loads(super(DateField, self).__call__())
        di.update(dict(dict(field=dict(xtype='datefield')),
                       dateFormat='Y-m-d H:i:s.u'))
        return json.dumps(di, indent=' ' * 4)


class TimeField(DefaultField):
    ext.adapts(IScaffoldingRecipeEditGrid, schema.interfaces.ITime)

    def __call__(self):
        di = json.loads(super(DateField, self).__call__())
        di.update(dict(dict(field=dict(xtype='timefield')),
                       dateFormat='H:i:s.u'))
        return json.dumps(di, indent=' ' * 4)


class FloatField(DefaultField):
    ext.adapts(IScaffoldingRecipeEditGrid, schema.interfaces.IFloat)

    def __call__(self):
        di = json.loads(super(FloatField, self).__call__())
        di.update(dict(field=dict(xtype='numberfield')))
        return json.dumps(di, indent=' ' * 4)


class IdField(column.DefaultField):
    ext.adapts(IScaffoldingRecipeEditGrid, schema.interfaces.IId)


class ChoiceField(DefaultField):
    ext.adapts(IScaffoldingRecipeEditGrid, schema.interfaces.IChoice)

    def __call__(self):
        di = json.loads(super(ChoiceField, self).__call__())
        # Create a combobox (same as form recipe)
        combobox = form.ChoiceField(self.recipe, self.field)()
        # But with empty fieldLabel
        combobox = combobox.replace(self.field.title, '')
        di.update(field="%combobox%")
        di['renderer'] = '%renderer%'
        di = json.dumps(di, indent=' ' * 4)
        di = di.replace('"%combobox%"', combobox)

        # Render the template
        tmpl = loader.load('combobox_renderer.json.tpl', cls=NewTextTemplate)
        stream = tmpl.generate(view=self)
        di = di.replace('"%renderer%"', stream.render())
        return di

    @property
    def terms(self):
        vr = getVocabularyRegistry()
        return vr.get(None, self.field.vocabularyName)
