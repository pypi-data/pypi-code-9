# -*- coding: utf-8 -*-
from django.db import models
# from django.db.models.query import QuerySet
from unicodedata import normalize

# class PostMixin(object):
#     def get_object(self):
#         return { 'ok': 'ok!' }
#
# class PostQuerySet(QuerySet, PostMixin):
#     pass
#
# class MyObjects(models.Manager, PostMixin):
#
#     def get_query_set(self):
#         return PostQuerySet(self.model, using=self._db)

class MyObjects(models.Manager):
    pass

class Pais(models.Model):
    """Países."""
    id = models.CharField(db_column="pais_id", max_length=3, primary_key=True)
    nome = models.CharField(db_column="pais_nome", max_length=64)
    numero = models.CharField(db_column="pais_numero", max_length=3)
    codigo = models.CharField(db_column="pais_codigo", max_length=2, unique=True)

    objects = MyObjects()

    class Meta:
        app_label = "repositories_public"
        db_table = u"public\".\"tb_pais"


class Estado(models.Model):

    """Estados."""
    id = models.AutoField(db_column="estado_id", primary_key=True)
    uf_id = models.IntegerField(db_column="uf_id", unique=True)
    nome = models.CharField(db_column="estado_nome", max_length=100)
    uf = models.CharField(db_column="estado_uf", max_length=2)

    objects = MyObjects()

    pais = models.ForeignKey('repositories_public.Pais', db_column="pais_id")

    class Meta:
        app_label = "repositories_public"
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

    estado = models.ForeignKey('repositories_public.Estado', db_column="uf_id")

    def get_object(self):
        dict = self.__dict__
        dict.pop("_django_version", None)
        dict.pop("_state", None)
        return dict

    class Meta:
        app_label = "repositories_public"
        db_table = u"public\".\"tb_cidade"


class Moeda(models.Model):

    """Moedas."""
    id = models.CharField(db_column="moeda_id", max_length=3, primary_key=True)
    nome = models.CharField(db_column="moeda_nome", max_length=64)

    objects = MyObjects()

    class Meta:
        app_label = "repositories_public"
        db_table = u"tb_moeda"


class Idioma(models.Model):

    """Idiomas."""
    id = models.CharField(db_column="idioma_id", max_length=5, primary_key=True)
    nome = models.CharField(db_column="idioma_nome", max_length=64)

    pais = models.ForeignKey('repositories_public.Pais', related_name="idiomas", default=None)

    objects = MyObjects()

    class Meta:
        app_label = "repositories_public"
        db_table = u"tb_idioma"


def remover_acentos(value):
    """Normalize the values."""
    try:
        return normalize('NFKD', value.decode('utf-8')).encode('ASCII', 'ignore')
    except UnicodeEncodeError:
        return normalize('NFKD', value).encode('ASCII', 'ignore')