# -*- coding: utf-8 -*-
from django.db import models
# from copy import copy
#from django.db.models.query import QuerySet

# from django.db.models.query import QuerySet


# class MyObjects(models.Manager):
#     def __init__(self, qs_class=models.query.QuerySet):
#         super(MyObjects,self).__init__()
#         self.queryset_class = qs_class
#
#     def get_query_set(self):
#         print 'x'
#         return self.queryset_class(self.model)
#
#     def __getattr__(self, attr, *args):
#         print 'y'
#         print args
#         print attr
#         try:
#             return getattr(self.__class__, attr, *args)
#         except AttributeError:
#             return getattr(self.get_query_set(), attr, *args)


# class PostMixin(object):
#     def by_author(self,):
#         print 'b'
#         return self.filter()
#
#     def published(self):
#         print 'a'
#         return self.filter()
#
#     def only(self, *args):
#         print 'xx'
#         print args
#         return super(PostMixin, self).get_query_set().only(*args)
#
#
# class PostQuerySet(QuerySet, PostMixin):
#     pass
#
# class PostQuerySet2(models.Manager, PostMixin):
#     pass

class MyObjects(models.Manager): #, PostMixin):
    pass
    # def get_queryset(self):
    #     print 'ai'
    #     return PostQuerySet(self.model, using=self._db)
    #
    # def get_query_set(self):
    #     print 'ia'
    #     return PostQuerySet(self.model, using=self._db)

    # def all(self,**kwargs):
    #     print 'y'
    #     return copy(super(MyObjects, self).all(**kwargs))
    #
    # def __init__(self):
    #     super(MyObjects, self).__init__()
    #
    # def filter(self, **kwargs):
    #     print 'x'
    #     # return PostQuerySet(self.model, using=self._db)
    #     return super(MyObjects, self).filter(**kwargs)

    # def only(self, *args):
    #     return PostQuerySet2()self.model, using=self._db, *args)
    #     # return super(MyObjects, self).only(*args)
    #
    # def get_context_data(self, **kwargs):
    #     print 'y'
    #
    # def get_object(self):
    #     print 'z'

    # def get_queryset(self):
    #     print 'larara'
    #
    #     for name, function in self.get_query_set.__dict__.items():
    #         print name
    #         print function
    #
    #     return super(MyObjects, self).get_queryset()

    # def raw(self):
    #     print 'yyyy'
    #     return super(MyObjects, self).raw()

# class PostQuerySet(QuerySet, MyObjects):
#     print 'xxxx'
#     pass
#
# class PostManager(models.Manager, MyObjects):
#     def get_query_set(self):
#         return PostQuerySet(self.model, using=self._db)

class Pais(models.Model):
    """Países."""
    id = models.CharField(db_column="pais_id", max_length=3, primary_key=True)
    nome = models.CharField(db_column="pais_nome", max_length=64)
    numero = models.CharField(db_column="pais_numero", max_length=3)
    codigo = models.CharField(db_column="pais_codigo", max_length=2, unique=True)

    objects = MyObjects()

    class Meta:
        app_label = "public"
        db_table = u"public\".\"tb_pais"


class Estado(models.Model):

    """Estados."""
    id = models.AutoField(db_column="estado_id", primary_key=True)
    uf_id = models.IntegerField(db_column="uf_id", unique=True)
    nome = models.CharField(db_column="estado_nome", max_length=100)
    uf = models.CharField(db_column="estado_uf", max_length=2)

    objects = MyObjects()

    pais = models.ForeignKey('public.Pais', db_column="pais_id")

    class Meta:
        app_label = "public"
        db_table = u"public\".\"tb_estado"


class Cidade(models.Model):

    """Cidades."""
    id = models.AutoField(db_column="cidade_id", primary_key=True)
    cidade = models.CharField(db_column="cidade", max_length=100)
    cidade_alt = models.CharField(db_column="cidade_alt", max_length=100)
    uf = models.CharField(db_column="uf", max_length=2)
    uf_munic = models.IntegerField(db_column="uf_munic")
    munic = models.IntegerField(db_column="munic")

    objects = MyObjects()

    estado = models.ForeignKey('public.Estado', db_column="uf_id")

    class Meta:
        db_table = u"public\".\"tb_cidade"
