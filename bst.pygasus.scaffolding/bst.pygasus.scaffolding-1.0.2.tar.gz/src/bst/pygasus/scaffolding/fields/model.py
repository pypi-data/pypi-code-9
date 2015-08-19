from zope import schema

from bst.pygasus.core import ext
from bst.pygasus.scaffolding.fields import BuilderBase
from bst.pygasus.scaffolding.interfaces import IScaffoldingRecipeModel


class ModelBuilderBase(BuilderBase):
    ext.baseclass()

    def base(self, overrides):
        b = dict(name=self.field.getName(),
                 useNull=not self.field.required)
        b.update(overrides)
        return b


class StringField(ModelBuilderBase):
    ext.adapts(IScaffoldingRecipeModel, schema.interfaces.IField)

    def __call__(self):
        return self.base(dict(type='string'))


class DateField(ModelBuilderBase):
    ext.adapts(IScaffoldingRecipeModel, schema.interfaces.IDate)

    def __call__(self):
        return self.base(dict(type='date',
                              dateFormat='Y-m-d H:i:s.u'))


class TimeField(ModelBuilderBase):
    ext.adapts(IScaffoldingRecipeModel, schema.interfaces.ITime)

    def __call__(self):
        return self.base(dict(type='date',
                              dateFormat='H:i:s.u'))


class IntField(ModelBuilderBase):
    ext.adapts(IScaffoldingRecipeModel, schema.interfaces.IInt)

    def __call__(self):
        return self.base(dict(type='int'))


class BoolField(ModelBuilderBase):
    ext.adapts(IScaffoldingRecipeModel, schema.interfaces.IBool)

    def __call__(self):
        return self.base(dict(type='boolean'))


class IdField(IntField):
    ext.adapts(IScaffoldingRecipeModel, schema.interfaces.IId)
