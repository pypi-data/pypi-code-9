# -*- coding: utf-8 -*-

__author__ = 'marcos.medeiros'

from django.forms import widgets
from django.template import loader, Context

from rapid.wrappers import ModelData, InstanceData

class RapidReadOnly(widgets.Widget):
    def __init__(self, *args, **kwargs):
        super(RapidReadOnly, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        hidden = '<input type="hidden" name="%s" value="%s" ' % (name, value)
        for a in attrs.keys():
            hidden += '%s="%s" ' % (a, attrs[a])
        hidden += '>'
        return '<span class="data-value">%s</span>%s\n' % (unicode(value), hidden)

    def value_from_datadict(self, data, files, name):
        return data[name]

class RapidRelationReadOnly(widgets.Widget):
    def __init__(self, model, *args, **kwargs):
        super(RapidRelationReadOnly, self).__init__(*args, **kwargs)
        self.model = ModelData(model)

    def render(self, name, value, attrs=None):
        hidden = '<input type="hidden" name="%s" value="%s" ' % (name, value)
        for a in attrs.keys():
            hidden += '%s="%s" ' % (a, attrs[a])
        hidden += '>'
        if hasattr(value, '__iter__'):
            objs = self.model.default_manager().filter(pk__in=value)
            ret = ''
            for o in objs:
                ret += '<span class="data-value multiple">%s</span>\n' % unicode(o)
            ret += hidden
            return ret
        else:
            obj = self.model.default_manager().get(pk=value)
            return '<span class="data-value">%s</span>%s\n' % (unicode(obj), hidden)

    def value_from_datadict(self, data, files, name):
        return data[name]


class RapidSelector(widgets.Select):
    """
    Selects one of the target crud type.
    For ForeignKeyFields and OneToOneFields.
    If the target is dependent (that means, has only
    value when linked with this object), only displays
    an edition link.
    """
    def __init__(self, relation, *args, **kwargs):
        super(RapidSelector, self).__init__(*args, **kwargs)
        self.relation = relation
        self.allow_multiple_selected = relation.is_multiple()
        self.remove_deselected = relation.is_weak()

    def render(self, name, value, attrs=None, choices=()):
        id = attrs.get('id', name)
        related = self.relation.related_model()
        if self.allow_multiple_selected:
            if value:
                v = ",".join([str(x) for x in value])
                selected = related.default_manager().filter(pk__in=value)
            else:
                v = ""
                selected = []
        else:
            if value:
                v = str(value)
                selected = related.default_manager().get(pk=value)
            else:
                v = ""
                selected = ""
        select_url = related.select_url()
        if self.allow_multiple_selected:
            icon = 'fa-times'
            if self.remove_deselected:
                icon = 'fa-trash-o'
        else:
            icon = 'fa-search'
        c = Context({'id': id, 'name': name, 'value': v, 'selected': selected, 'icon': icon, 'select_url': select_url,
                     'multiple': self.allow_multiple_selected})
        if self.allow_multiple_selected:
            t = loader.get_template('rapid/widgets/multiple-selector.html')
        else:
            t = loader.get_template('rapid/widgets/single-selector.html')
        return t.render(c)

    def value_from_datadict(self, data, files, name):
        val = data.get(name)
        if self.allow_multiple_selected:
            if val:
                return [int(x) for x in val.split(",") if x]
            return []
        else:
            if val:
                return int(val)
            return None

