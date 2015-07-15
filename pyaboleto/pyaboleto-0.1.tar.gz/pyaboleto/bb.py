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


from pyaboleto import *


banco_brasil = Banco('001', 'Banco do Brasil')

class BBBoleto(Boleto):

    def _validar_convenio(self, tam_conv, tam_nos_num):
        if not re.match('^\d{%d}\-\d$' % tam_nos_num, self.nosso_numero):
            raise PYABoletoExcpetion('Para convênio de %d posições o Nosso Número deve conter %d dígitos, '
                                     '1 hífen e 1 dv (%s-0)' % (tam_conv, tam_nos_num, str.zfill('0', tam_nos_num)))

    def _validar_codigo_barras(self):
        """
        Como a classe ancestral já valida os campos padronizados pela FEBRABAN basta
        validar os campos necessários ao Campo Livre.
        """
        super(BBBoleto, self)._validar_codigo_barras()

        self._validar_digitos(self.convenio.carteira, 2, 'carteira')
        self._validar_digitos(self.convenio.agencia, 4, 'agência', True)
        self._validar_digitos(self.convenio.conta, 8, 'conta', True)

        if len(self.convenio.numero) not in (4, 6, 7):
            raise PYABoletoExcpetion('O número do convênio deve ter 4 (0000), 6 (000000) ou 7 (0000000) dígitos')

        tam_conv = len(self.convenio.numero)
        if self.convenio.carteira == '21':
            if tam_conv != 6:
                raise PYABoletoExcpetion('Para Carteiras 16 e 18 (Tipo de Modalidade de Cobrança 21) '
                                         'o Número do Convênio deve ter 6 posições')
            if not re.match('^\d{17}$', self.nosso_numero):
                raise PYABoletoExcpetion('Para Carteiras 16 e 18 (Tipo de Modalidade de Cobrança 21) o '
                                         'Nosso Número deve conter 17 dígitos sem hífen e sem 1 dv (00000000000000000)')
        if tam_conv == 4:
            self._validar_convenio(tam_conv, 7)
        elif tam_conv == 6:
            if self.convenio.carteira != '21':
                self._validar_convenio(tam_conv, 5)
        elif tam_conv == 7:
            self._validar_convenio(tam_conv, 10)

    @property
    def campo_livre(self):
        """
        Gera o campo livre do código de barras.
        """
        self._validar_codigo_barras()
        sem_dv = -2
        if len(self.convenio.numero) == 4:
            return '%4s%7s%4s%8s%2s' % (self.convenio.numero,
                                        self.nosso_numero[:sem_dv],
                                        self.convenio.agencia[:sem_dv],
                                        self.convenio.conta[:sem_dv],
                                        self.convenio.carteira)
        elif len(self.convenio.numero) == 6 and self.convenio.carteira != '21':
            return '%6s%5s%4s%8s%2s' % (self.convenio.numero,
                                        self.nosso_numero[:sem_dv],
                                        self.convenio.agencia[:sem_dv],
                                        self.convenio.conta[:sem_dv],
                                        self.convenio.carteira)
        elif len(self.convenio.numero) == 6 and self.convenio.carteira == '21':
            return '%6s%17s%2s' % (self.convenio.numero,
                                   self.nosso_numero,
                                   self.convenio.carteira)
        elif len(self.convenio.numero) == 7:
            return '000000%7s%10s%2s' % (self.convenio.numero,
                                         self.nosso_numero[:sem_dv],
                                         self.convenio.carteira)
