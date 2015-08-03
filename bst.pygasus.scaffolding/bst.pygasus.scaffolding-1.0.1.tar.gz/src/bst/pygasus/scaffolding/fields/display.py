import json
from zope import schema
from zope.i18n import translate
from zope.schema.vocabulary import getVocabularyRegistry

from bst.pygasus.core import ext
from bst.pygasus.scaffolding import loader
from bst.pygasus.scaffolding.fields import BuilderBase
from bst.pygasus.scaffolding.interfaces import IScaffoldingRecipeDisplay

from genshi.template import NewTextTemplate

class BuilderDefaultForm(BuilderBase):
    ext.adapts(IScaffoldingRecipeDisplay, schema.interfaces.IField)

    def __call__(self):
        di = dict(xtype='displayfield',
                  name=self.field.getName(),
                  fieldLabel=translate(self.field.title,
                                       context=self.recipe.request)
                  )
        return json.dumps(di, indent=' ' * 4)


class ChoiceField(BuilderDefaultForm):
    ext.adapts(IScaffoldingRecipeDisplay, schema.interfaces.IChoice)

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
