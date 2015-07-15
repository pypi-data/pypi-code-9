# -*- coding: utf-8 -*-
"""
The MIT License (MIT)

Copyright 2015 Umbrella Tech.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
__author__ = 'Kelson da Costa Medeiros <kelsoncm@gmail.com>'

from datetime import date
import re


def raiser(invalido, mensagem):
    if invalido:
        raise PYABoletoExcpetion(mensagem)


def modulo11(numero, if_dez='0', if_zero='0', mascarado=False, max_fator=9, separador='-'):
    soma = 0
    fator = 2
    for c in reversed(numero):
        soma += int(c) * fator
        fator = 2 if fator >= max_fator else fator + 1;

    resto = (soma * 10) % 11
    if resto == 10:
        resto = if_dez
    elif resto == 0:
        resto = if_zero
    return str(resto if not mascarado else '%s%s%s' % (numero, separador, resto))

def modulo10(number):
    soma = 0
    fato = 2
    for c in reversed(number):
        tmp = int(c) * fato
        if tmp > 9:
            tmp = tmp - 10 + 1
        soma += tmp
        fato = 2 if fato == 1 else 1

    resto = soma % 10
    return str(10 - resto if resto != 0 else 0)


class PYABoletoExcpetion(Exception):
    def __init__(self, message):
        super(PYABoletoExcpetion, self).__init__(message)


class Endereco:

    """
    Classe abstrata que representa uma pessoa, física ou jurídica.
    """

    # end = Endereco('12345-123', 'Av. Imortais', '666', 'Ap. 23', 'Academia', 'Brasileira', 'LT', 'BR')
    # end = Endereco('12345-123', 'Av. Imortais da Academia', '666', 'Academia', 'Brasileira', 'Letras')

    def __init__(self,  cep, logradouro, numero, complemento, bairro, cidade, uf, pais='Brasil'):
        self.cep = cep
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.uf = uf
        self.pais = pais

    def __str__(self):
        if self.complemento:
            '''Av. Fernando Pessoa 1234, Ap. 192, Imortais, Academia-AL, Brasil, CEP: 12345-123'''
            return '%s %s, %s, %s, %s-%s, %s, CEP: %s' % \
                   (self.logradouro, self.numero, self.complemento, self.bairro, self.cidade, self.uf, self.pais, self.cep)

        '''Av. Fernando Pessoa 1234, Imortais, Academia-AL, Brasil, CEP: 12345-123'''
        return '%s %s, %s, %s-%s, %s, CEP: %s' % \
               (self.logradouro, self.numero, self.bairro, self.cidade, self.uf, self.pais, self.cep)


class Pessoa:
    """
    Classe abstrata que representa uma pessoa, física ou jurídica.
    """

    def __init__(self, nome, cpf_cnpj, endereco, documento_pessoal=None):
        """
        Inicializa uma nova instância da classe.
        """
        self.nome = nome
        self.cpf_cnpj = cpf_cnpj
        self.endereco = endereco
        self.documento_pessoal = documento_pessoal

    def __str__(self):
        if self.documento_pessoal:
            return '%s - %s - %s - %s' % (self.nome, self.cpf_cnpj, self.documento_pessoal, self.endereco)
        return '%s - %s - %s' % (self.nome, self.cpf_cnpj, self.endereco)


class Sacado(Pessoa):
    # sac = Sacado('Kelson C. Medeiros', '123.456.789-01', end, '123465 SSP/UF')
    # sac = Sacado('Kelson C. Medeiros', '123.456.789-01', end)
    pass


class Cedente(Pessoa):
    # ced = Cedente('Kelson C. Medeiros', '12.345.678/9012-34', end)
    # ced = Cedente('Kelson C. Medeiros', '12.123.123/0001-12', end)
    pass


class Banco:
    """
    Classe abstrata que representa um banco.
    """

    # ban = Banco('001', 'Banco do Brasil')

    def __init__(self, numero, nome):
        self.numero = numero
        self.nome = nome

    def __str__(self):
        return "%s" % self.numero

class Convenio:
    """
    Classe abstrata que representa o convênio.
    """

    # con = Convenio(ban, car, '123456', '12345678')

    def __init__(self, numero, carteira, banco, agencia, conta):
        self.carteira = carteira
        self.numero = numero
        self.banco = banco
        self.agencia = agencia
        self.conta = conta

    def __str__(self):
        return "%s - %s, %s - %s - %s" % (self.numero, self.carteira, self.banco, self.agencia, self.conta)

class Boleto:
    """
    Classe abstrata que representa um boleto.
    """

    DATA_BASE = date(1997, 10, 7)

    # bol = Boleto(sac, ced, con, 123.45, date(2015, 12, 12), '123456789')

    def __init__(self, nosso_numero, data_vencimento, valor_documento, convenio, cedente, sacado):
        self.sacado = sacado
        self.cedente = cedente
        self.convenio = convenio
        self.valor_documento = valor_documento
        self.data_vencimento = data_vencimento
        self.data_documento = date.today()
        self.nosso_numero = nosso_numero
        self.taxa = 0
        self.desconto = 0
        self.outra_deducoes = 0
        self.multa = 0
        self.outros_acrescimos = 0
        self.instrucoes = ''
        self.demonstrativo = ''
        self.quantidade = 0
        self.aceite = None
        self.especie = None
        self.local_pagamento = None
        self.erros = []
        self.moeda = '9'

    def __str__(self):
        return self.linha_digitavel

    @property
    def total(self):
        return (self.valor_documento + self.taxa + self.outros_acrescimos) - (self.desconto + self.outra_deducoes)

    @property
    def fator_vencimento(self):
        delta = self.data_vencimento - Boleto.DATA_BASE
        return str.zfill(str(delta.days), 4)

    @property
    def campo_livre(self):
        return str.zfill('0', 25)

    @property
    def valor_plano(self):
        return str.zfill(str(int(self.total * 100)), 10)

    @staticmethod
    def _validar_digitos(valor, digitos, campo, mascarar=False):
        if mascarar:
            if not re.match('^\d{%d}\-\d$' % digitos, valor):
                raise PYABoletoExcpetion('O campo %s deve conter %d digitos, 1 hífen e 1 dv (%s-0)' %
                                         (campo, digitos, str.zfill('0', digitos)))
        else:
            if not re.match('^\d{%d}$' % digitos, valor):
                raise PYABoletoExcpetion('O campo %s deve conter %d digitos (%s)' %
                                         (campo, digitos, str.zfill('0', digitos)))

    def _validar_codigo_barras(self):
        if not re.match('\d{3}', str(self.convenio.banco)):
            raise PYABoletoExcpetion('O banco deve conter 3 digitos (000)')

        if not re.match('^\d$', str(self.moeda)):
            raise PYABoletoExcpetion('A moeda deve conter 1 digito (0)')

        if int(self.valor_plano) > 9999999999:
            raise PYABoletoExcpetion('O valor total deve ser menor que 99999999.99')


    @property
    def codigo_barras(self):
        """
        Campo Livre definido por cada banco.
        Os outros campos do código de barras é fixo. A linha digitável também é fixo.

        Posição  #   Conteúdo
        01 a 03  03  Número do banco
        04       01  Código da Moeda - 9 para Real
        05       01  Digito verificador do Código de Barras
        06 a 09  04  Data de vencimento em dias a partir de 07/10/1997
        10 a 19  10  Valor do boleto (8 inteiros e 2 decimais)
        20 a 44  25  Campo Livre definido por cada banco
        Total    44
        """

        self._validar_codigo_barras()

        campo_livre = self.campo_livre

        if not re.match('^\d{25}$', str(campo_livre)):
            raise PYABoletoExcpetion('O campo livre deve conter 25 digito (0000000000000000000000000)')

        temp = "%3s%1s%4s%10s%25s" % \
               (self.convenio.banco, self.moeda, self.fator_vencimento, self.valor_plano, campo_livre)

        dv = modulo11(temp, 1, 1)

        return temp[:4] + dv + temp[4:]

    @property
    def linha_digitavel(self):
        """
        Gera a linha digitável (formatada) baseado em um código de barras.

        Campo1 - 1 a 4 e 20 a 24 - Banco + Moeda + Campo Livre de 1 a 4
        Campo2 - 25 a 34         - Campo Livre de 5 a 14
        Campo3 - 35 a 44         - Campo Livre de 15 a 25
        Campo4 - 5               - DV do Código de Barras
        Campo5 - 6 a 19          - Data de vencimento + Valor do boleto

        AAABC.CCCCX DDDDD.DDDDDY EEEEE.EEEEEZ K UUUUVVVVVVVVVV
        A = Código do BB na COMPE
        B = Código da moeda (9 - Real)
        C = Posições 20 a 24 do código de barras
        X = DV do Campo 1 (Módulo 10, cálculo conforme anexo 7)
        D = Posições 25 a 34 do código de barras
        Y = DV do Campo 2 (Módulo 10, cálculo conforme anexo 7)
        F = Posições 35 a 44 do código de barras
        Z =DV do Campo 3 (Módulo 10, cálculo conforme anexo 7)
        K = DV do código de barras (Módulo 10, cálculo conforme anexo 107)
        U = Fator de Vencimento (Módulo 10, cálculo conforme anexo 8)
        V = Valor do título (com duas casas decimais, sem ponto e vírgula. Em caso de moeda variável, informar zeros)
        """
        def monta_campo(campo):
            campo_dv = "%s%s" % (campo, modulo10(campo))
            return "%s.%s" % (campo_dv[0:5], campo_dv[5:])

        linha = self.codigo_barras

        return ' '.join([monta_campo(linha[0:4] + linha[19:24]),
                         monta_campo(linha[24:34]),
                         monta_campo(linha[34:44]),
                         linha[4],
                         linha[5:19]])
