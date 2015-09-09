# -*- coding: utf-8 -*-
from ..models import MyObjects

from django.db import models


class CupomDesconto(models.Model):
    """Cupom de desconto."""
    TIPO_VALOR_FIXO = 'fixo'
    TIPO_PORCENTAGEM = 'porcentagem'
    TIPO_FRETE_GRATIS = 'frete_gratis'

    CHOICES_CUPOM_TIPOS = [
        (TIPO_VALOR_FIXO, u'Valor fixo'),
        (TIPO_PORCENTAGEM, u'Porcentagem'),
        (TIPO_FRETE_GRATIS, u'Frete grátis'),
    ]

    id = models.AutoField(db_column="cupom_desconto_id", primary_key=True)
    descricao = models.TextField(db_column="cupom_desconto_descricao")
    codigo = models.CharField(db_column="cupom_desconto_codigo", max_length=32)
    valor = models.DecimalField(db_column='cupom_desconto_valor', max_digits=16, decimal_places=2, null=True)
    tipo = models.CharField(db_column="cupom_desconto_tipo", max_length=32, choices=CHOICES_CUPOM_TIPOS)
    cumulativo = models.BooleanField(db_column="cupom_desconto_acumulativo", default=False)
    quantidade = models.IntegerField(db_column="cupom_desconto_quantidade")
    quantidade_por_cliente = models.IntegerField(db_column="cupom_desconto_quantidade_por_usuario", null=True)
    quantidade_usada = models.IntegerField(db_column="cupom_desconto_quantidade_utilizada", default=0)
    validade = models.DateTimeField(db_column="cupom_desconto_validade", null=True)
    valor_minimo = models.DecimalField(db_column='cupom_desconto_valor_minimo', max_digits=16, decimal_places=2, null=True)
    data_criacao = models.DateTimeField(db_column="cupom_desconto_data_criacao", auto_now_add=True)
    data_modificacao = models.DateTimeField(db_column="cupom_desconto_data_modificacao", auto_now=True)
    ativo = models.BooleanField(db_column="cupom_desconto_ativo", default=False)
    aplicar_no_total = models.BooleanField(db_column='cupom_desconto_aplicar_no_total', default=False, null=False)

    objects = MyObjects()

    conta = models.ForeignKey("repositories_plataforma.Conta", related_name='cupons')
    contrato = models.ForeignKey("repositories_plataforma.Contrato", related_name='cupons')

    class Meta:
        app_label = "repositories_marketing"
        db_table = u"marketing\".\"tb_cupom_desconto"
        verbose_name = u'Cupom de desconto'
        verbose_name_plural = u"Cupons de desconto"
        ordering = ['codigo']
        unique_together = (("conta", "codigo"),)

    def __unicode__(self):
        return self.codigo


class SEO(models.Model):
    """S.E.O."""
    id = models.AutoField(db_column="seo_id", primary_key=True)
    tabela = models.CharField(db_column="seo_tabela", max_length=64)
    linha_id = models.IntegerField(db_column="seo_linha_id")
    data_criacao = models.DateTimeField(db_column="seo_data_criacao", auto_now_add=True)
    data_modificacao = models.DateTimeField(db_column="seo_data_modificacao", auto_now=True)
    title = models.CharField(db_column="seo_title", max_length=255, null=True)
    keyword = models.CharField(db_column="seo_keyword", max_length=255, null=True)
    description = models.CharField(db_column="seo_description", max_length=255, null=True)
    robots = models.CharField(db_column="seo_robots", max_length=32, null=True)

    idioma = models.ForeignKey('repositories_public.Idioma', related_name="seos", default='pt-br')
    conta = models.ForeignKey("repositories_plataforma.Conta", related_name="seos")
    contrato = models.ForeignKey("repositories_plataforma.Contrato", related_name="seos")

    class Meta:
        app_label = "repositories_marketing"
        db_table = u"marketing\".\"tb_seo"