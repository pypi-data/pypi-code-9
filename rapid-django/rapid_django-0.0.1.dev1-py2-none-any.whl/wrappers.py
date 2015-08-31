# -*- coding: utf-8 -*-

__author__ = 'marcos.medeiros'

from rapid.registry import registry, Action
from rapid import filters

import itertools
from django.db import models


class InstanceData:
    def __init__(self, instance, request=None, excludes=None, creator=None, fields=None):
        excludes = [] if excludes is None else excludes
        self.model = ModelData(type(instance), request, excludes, creator, fields)
        self.instance = instance
        self.request = request
        self.excludes = excludes if excludes else []
        self.creator = creator
        self._fields = fields if fields else self.model.fields()

    def values(self):
        o = self.instance
        for f in self.model.fields():
            if f.is_relation:
                yield self._value_of_field(o, f)
            else:
                yield self._value_of_field(o, f)

    def _value_of_field(self, instance, field):
        """
        Retorna o valor do campo dado na instância informada.
        ::return Uma tupla, onde o primeiro elemento é o valor informado, o
        segundo elemento é um booleano que informa se o valor é iteravel ou não
        e o terceiro elemento é uma sequencia de URLs para os itens do primeiro elemento,
        ou um valor falso caso não haja links.
        """
        if hasattr(instance, field.bare_name()):
            v = getattr(instance, field.bare_name())
        else:  # Many to many relations without value may disappear
            return [], True
        if hasattr(v, '__iter__'):
            return (v, ()), True
        if hasattr(v, 'all'):
            return [(x, InstanceData(x, self.request, creator=(self, field))) for x in v.all()], True
        if isinstance(v, models.Model):
            return (v, InstanceData(v, self.request, creator=(self, field))), False
        return (v, ()), False

    def fields_and_values(self):
        for field in self.model.fields():
            value, is_multiple = self._value_of_field(self.instance, field)
            yield field, value, is_multiple

    def is_controlled(self):
        return self.model.is_controlled()

    def can_read(self):
        if self.can_write():
            return True
        vw = registry.model_entry(self.model.model).permission_set(self.request)
        if vw:
            return vw.filter(pk=self.instance.pk).exists()
        return False

    def can_write(self):
        ed = registry.model_entry(self.model.model)['edit'].permission_set(self.request)
        if ed:
            return ed.filter(pk=self.instance.pk).exists()
        return False

    def view_url(self):
        return registry.get_url_of_action(self.model.model, "view", pk=self.instance.pk)

    def edit_url(self):
        url = registry.get_url_of_action(self.model.model, "edit", pk=self.instance.pk)
        by = self.creator
        if by:
            dt, fd = by
            if fd.one_to_one or fd.one_to_many:
                # Este objeto depende do parent.
                # Não posso editar esta relação
                return url + "?default=" + fd.field.name + ":" + str(dt.object.pk)
            if fd.many_to_one or fd.many_to_many:
                return url
        return url

    def remove_url(self):
        return registry.get_url_of_action(self.model.model, "delete", pk=self.instance.pk)

    def create_url(self):
        return registry.get_url_of_action(self.model.model, "add")

    def list_url(self):
        return registry.get_url_of_action(self.model.model, "list")

    def select_url(self):
        return registry.get_url_of_action(self.model.model, "select")

    def actions(self):
        acts = registry.model_entry(self.model.model)
        if self.request:
            for a in acts.values():
                if a.permission_set(self.request) and\
                        a.permission_set(self.request).filter(pk=self.instance.pk).exists() and\
                        a.action.visibility > Action.Visibility.hidden:
                    yield (a, a.get_url(self.instance))

    def model_actions(self):
        for (a, u) in self.actions():
            if not a.action.query_parameters:
                yield (a, u)

    def instance_actions(self):
        for (a, u) in self.actions():
            if a.action.query_parameters:
                yield (a, u)

    def list_actions(self):
        for (a, u) in self.instance_actions():
            if a.action.visibility == Action.Visibility.list:
                yield (a, u)

    def has_permission(self, request, action_name):
        m = registry.model_entry(self.model.model).get(action_name)
        if m:
            return m.permission_set(request) and\
                m.permission_set(request).filter(pk=self.instance.pk).exists()
        return False

    def __unicode__(self):
        return unicode(self.instance)

    def __str__(self):
        return str(self.model) + ': ' + str(self.instance.pk)


class ModelData:
    def __init__(self, model, request=None, excludes=None, creator=None, fields=None):
        excludes = [] if excludes is None else excludes
        self.model = model
        self.request = request
        self.excludes = excludes if excludes else []
        self.creator = creator
        self._fields = [self.field_by_name(f) for f in fields] if fields else self.all_fields()

    def model_name(self):
        return unicode(self.model._meta.verbose_name)

    def model_name_plural(self):
        return unicode(self.model._meta.verbose_name_plural)

    def default_manager(self):
        return self.model._default_manager

    def all_fields(self):
        relations = []
        for f in itertools.chain(self.local_fields(), self.related_fields()):
            if f.is_relation():
                relations.append(f)
            else:
                if f.name not in self.excludes:
                    yield f
        for f in relations:
            if f.name not in self.excludes:
                yield f

    def fields(self):
        for f in self._fields:
            yield f

    def local_fields(self):
        for f in self.model._meta.local_fields:
            if f.name not in self.excludes:
                yield FieldData(f, self.request)
        for f in self.model._meta.local_many_to_many:
            if f.name not in self.excludes:
                yield FieldData(f, self.request)

    def related_fields(self):
        for f in self.model._meta.get_all_related_objects():
            yield FieldData(f, self.request)

    def is_controlled(self):
        return registry.is_controlled(self.model)

    def can_read(self):
        if self.can_write():
            return True
        vw = registry.model_entry(self.model)['view'].permission_set(self.request)
        if vw:
            return vw.exists()
        return False

    def can_write(self):
        ed = registry.model_entry(self.model)['edit'].permission_set(self.request)
        if ed:
            return ed.exists()
        return False

    def create_url(self):
        return registry.get_url_of_action(self.model, "add")

    def list_url(self):
        return registry.get_url_of_action(self.model, "list")

    def select_url(self):
        return registry.get_url_of_action(self.model, "select")

    def actions(self):
        acts = registry.model_entry(self.model)
        if self.request:
            for a in acts.values():
                if a.permission_set(self.request) and\
                        a.permission_set(self.request).exists() and\
                        not a.action.query_parameters and\
                        a.action.visibility > Action.Visibility.hidden:
                    yield (a, a.get_url())

    def has_permission(self, request, action_name):
        m = registry.model_entry(self.model).get(action_name)
        if m:
            return m.permission_set(request) and\
                m.permission_set(request).exists()
        return False

    def field_by_name(self, field_name):
        return FieldData(self.model._meta.get_field(field_name), self.request)

    def __unicode__(self):
        return unicode(self.model)

    def __str__(self):
        return 'Model: ' + str(self.model)


class FieldData:
    def __init__(self, field, request=None):
        self.field = field
        self.request = request

    @classmethod
    def from_model(cls, model, field_name):
        ff = ModelData(model).fields()
        for f in ff:
            if f.bare_name() == unicode(field_name):
                return f
        return None

    def bare_name(self):
        return unicode(self.field.name)

    def name(self):
        if hasattr(self.field, "verbose_name"):
            return unicode(self.field.verbose_name)
        return unicode(self.field.name)

    def name_plural(self):
        if hasattr(self.field, "verbose_name_plural"):
            return unicode(self.field.verbose_name_plural)
        return self.name() + "s"

    def is_relation(self):
        return self.field.is_relation

    def is_multiple(self):
        if not self.is_relation():
            return False
        if self.field.one_to_many:
            return True
        if self.field.many_to_many:
            return True
        return False

    def related_model(self):
        if hasattr(self.field, "related_model"):
            return ModelData(self.field.related_model)
        if hasattr(self.field, "to"):
            return ModelData(self.field.to)
        return None

    def is_weak(self):
        if not self.is_relation():
            return False
        f = self.field
        if hasattr(f, "many_to_many") and f.many_to_many:
            return False
        if hasattr(f, "many_to_one") and self.field.many_to_one:
            return False
        if hasattr(self.field, "get_related_field"):
            o = self.field.get_related_field
            if self.field.one_to_one or self.field.one_to_many:
                if hasattr(o, "required"):
                    return o.required
                return True
        if isinstance(f, models.ForeignKey):
            return self.related_model()._meta.pk.name
        return False

    def filter_html(self):
        return filters.Filter.selection_type_html(self, self.request)

    def __str__(self):
        return self.bare_name()


class ValueData:
    def __init__(self, value, field):
        self.value = value
        self.field = field

    def can_view(self):
        if self.field.is_relation():
            o = self.field.related_model()
            return registry.is_controlled(o)
        return False

    def is_multiple(self):
        return self.field.is_multiple()

    def __str__(self):
        return str(self.field) + ': ' + str(self.value)
