# coding: utf-8

from django.db.models import ManyToManyField, ForeignKey

from . import widgets as w


class StickyFileField(ForeignKey):
    widget_class = w.OneFileWidget

    def __init__(self, to, *args, **kwargs):
        self.max_objects = kwargs.pop('max_objects', None)
        self.to_app, self.to_model = to.split('.')
        super(StickyFileField, self).__init__(to, *args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = self.widget_class(
            to_app=self.to_app,
            to_model=self.to_model,
        )
        return super(StickyFileField, self).formfield(**kwargs)


class StickyImageField(StickyFileField):
    widget_class = w.OneImageWidget


class ManyStickyFileField(ManyToManyField):
    widget_class = w.ManyFileWidget

    def __init__(self, to, *args, **kwargs):
        self.max_objects = kwargs.pop('max_objects', None)
        self.to_app, self.to_model = to.split('.')
        super(ManyStickyFileField, self).__init__(to, *args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = self.widget_class(
            max_objects=self.max_objects,
            to_app=self.to_app,
            to_model=self.to_model,
        )
        return super(ManyStickyFileField, self).formfield(**kwargs)


class ManyStickyImageField(ManyStickyFileField):
    widget_class = w.ManyImageWidget
